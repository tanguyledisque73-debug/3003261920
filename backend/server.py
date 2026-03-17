from fastapi import FastAPI, APIRouter, HTTPException, Depends, Query, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import hashlib
import secrets
import random
import string
import shutil
import asyncio
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import BytesIO

# PDF Generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# SMTP Configuration (Infomaniak)
SMTP_HOST = os.environ.get('SMTP_HOST', 'mail.infomaniak.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'contact@secours73.fr')
SENDER_NAME = os.environ.get('SENDER_NAME', 'Secours Alpes 73')

# Logger
logger = logging.getLogger(__name__)

async def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Send email via SMTP (Infomaniak)"""
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning("SMTP credentials not configured, skipping email")
        return False
    
    try:
        message = MIMEMultipart("alternative")
        message["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            start_tls=True
        )
        logger.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

# Upload directory
UPLOAD_DIR = Path("/app/uploads")
VIDEO_UPLOAD_DIR = UPLOAD_DIR / "videos"
VIDEO_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Create the main app
app = FastAPI(title="Secours 73 API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# ============== MODELS ==============

# Auth Models
class UserCreate(BaseModel):
    email: str
    password: str
    nom: str
    prenom: str
    code_groupe: Optional[str] = None  # Required for stagiaires

class UserLogin(BaseModel):
    email: str
    password: str

class AdminCreateFormateur(BaseModel):
    email: str
    nom: str
    prenom: str

class UserResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    email: str
    nom: str
    prenom: str
    role: str
    created_at: str
    must_set_password: Optional[bool] = False

# Groupe de Formation Models
class GroupeFormationCreate(BaseModel):
    nom: str
    formation_type: str = "PSE"  # PSE, BNSSA, PSC
    seuil_reussite: int = 80  # Minimum 80%
    chapitres_ordre: List[str] = []  # Ordered list of chapter IDs

class GroupeFormationUpdate(BaseModel):
    nom: Optional[str] = None
    seuil_reussite: Optional[int] = None
    chapitres_ordre: Optional[List[str]] = None
    is_active: Optional[bool] = None

class GroupeFormationResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    nom: str
    code_acces: str
    formateur_id: str
    formation_type: str
    seuil_reussite: int
    chapitres_ordre: List[str]
    collaborateurs: List[str]
    nb_stagiaires: int
    max_stagiaires: int
    is_active: bool
    created_at: str

# Quiz Models
class QuizQuestionCreate(BaseModel):
    question: str
    type: str  # "qcm" ou "vrai_faux"
    options: List[str]
    correct_answer: int
    explication: str

class QuizCreate(BaseModel):
    chapter_id: str
    titre: str
    video_url: Optional[str] = None
    questions: List[QuizQuestionCreate]

class QuizUpdate(BaseModel):
    titre: Optional[str] = None
    video_url: Optional[str] = None
    questions: Optional[List[QuizQuestionCreate]] = None

class QuizQuestion(BaseModel):
    id: str
    question: str
    type: str
    options: List[str]
    correct_answer: int
    explication: str

class QuizResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    chapter_id: str
    titre: str
    video_url: Optional[str] = None
    questions: List[QuizQuestion]

class QuizSubmission(BaseModel):
    quiz_id: str
    answers: List[int]

class QuizResultResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    user_id: str
    quiz_id: str
    chapter_id: str
    score: int
    total: int
    percentage: float
    answers: List[dict]
    completed_at: str

# Chapter Models
class ChapterResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    numero: int
    titre: str
    description: str
    icon: str
    fiches: List[dict]
    formation_type: str

class FicheCreate(BaseModel):
    titre: str
    contenu: str

class ChapterCreate(BaseModel):
    numero: int
    titre: str
    description: str
    icon: str
    formation_type: str = "PSE"
    fiches: List[FicheCreate]

# Progress Models
class StagiaireProgressResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_id: str
    groupe_id: str
    chapitres_debloques: List[str]
    chapitres_completes: List[str]
    quizzes_completed: int
    average_score: float

# Collaboration invite
class CollaborationInvite(BaseModel):
    formateur_email: str
    groupe_id: str

# Site Settings Models
class SiteSettingsUpdate(BaseModel):
    helloasso_url: Optional[str] = None
    helloasso_enabled: Optional[bool] = None

class SiteImageCreate(BaseModel):
    name: str
    url: str
    alt_text: str
    section: str  # "hero", "pse", "bnssa", "psc", "about"
    order: int = 0

class SiteImageUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    alt_text: Optional[str] = None
    section: Optional[str] = None
    order: Optional[int] = None

# Document Models
class DocumentUpload(BaseModel):
    titre: str
    categorie: str  # "Cours", "Certificats", "Évaluations"
    description: Optional[str] = None
    destinataire_type: str  # "groupe" ou "stagiaire"
    groupe_id: Optional[str] = None
    stagiaire_id: Optional[str] = None

class DocumentResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    titre: str
    categorie: str
    description: Optional[str]
    filename: str
    file_size: int
    formateur_id: str
    formateur_nom: str
    destinataire_type: str
    groupe_id: Optional[str]
    stagiaire_id: Optional[str]
    uploaded_at: str

# ============== HELPER FUNCTIONS ==============

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token() -> str:
    return secrets.token_hex(32)

def generate_code_groupe() -> str:
    """Generate a unique 8-character group code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Simple token storage
active_tokens = {}

async def get_current_user(token: str) -> dict:
    if not token or token not in active_tokens:
        raise HTTPException(status_code=401, detail="Token invalide")
    user_id = active_tokens[token]
    user = await db.users.find_one({"id": user_id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
    return user

async def require_admin(token: str) -> dict:
    user = await get_current_user(token)
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    return user

async def require_formateur(token: str) -> dict:
    user = await get_current_user(token)
    if user["role"] not in ["formateur", "admin"]:
        raise HTTPException(status_code=403, detail="Accès réservé aux formateurs")
    return user

async def require_stagiaire(token: str) -> dict:
    user = await get_current_user(token)
    if user["role"] != "stagiaire":
        raise HTTPException(status_code=403, detail="Accès réservé aux stagiaires")
    return user

async def require_auth(token: str) -> dict:
    """Generic auth check - allows any authenticated user"""
    return await get_current_user(token)

# ============== AUTH ROUTES ==============

@api_router.post("/auth/register")
async def register(user_data: UserCreate):
    """Register a new stagiaire with a group code"""
    # Check if email exists
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")
    
    # Validate group code for stagiaires
    if not user_data.code_groupe:
        raise HTTPException(status_code=400, detail="Un code de groupe est requis pour l'inscription")
    
    groupe = await db.groupes_formation.find_one({"code_acces": user_data.code_groupe, "is_active": True}, {"_id": 0})
    if not groupe:
        raise HTTPException(status_code=400, detail="Code de groupe invalide ou inactif")
    
    # Check max stagiaires
    current_count = await db.users.count_documents({"groupe_id": groupe["id"]})
    if current_count >= groupe["max_stagiaires"]:
        raise HTTPException(status_code=400, detail="Ce groupe a atteint le nombre maximum de stagiaires (18)")
    
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": user_data.email,
        "password": hash_password(user_data.password),
        "nom": user_data.nom,
        "prenom": user_data.prenom,
        "role": "stagiaire",
        "groupe_id": groupe["id"],
        "formateur_id": groupe["formateur_id"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "must_set_password": False
    }
    
    await db.users.insert_one(user)
    
    # Initialize stagiaire progress
    progress = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "groupe_id": groupe["id"],
        "chapitres_debloques": [groupe["chapitres_ordre"][0]] if groupe["chapitres_ordre"] else [],
        "chapitres_completes": [],
        "quiz_results": []
    }
    await db.stagiaire_progress.insert_one(progress)
    
    # Send welcome email (non-blocking, don't fail registration if email fails)
    try:
        import asyncio
        asyncio.create_task(send_welcome_email_internal(user_data.email, user_data.prenom))
    except Exception as e:
        logger.warning(f"Failed to send welcome email: {str(e)}")
    
    # Auto login
    token = generate_token()
    active_tokens[token] = user_id
    
    return {
        "token": token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "nom": user["nom"],
            "prenom": user["prenom"],
            "role": user["role"],
            "groupe_id": user["groupe_id"]
        }
    }

@api_router.post("/auth/register-visiteur")
async def register_visiteur(user_data: UserCreate):
    """Register a free visitor account (limited access)"""
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")
    
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": user_data.email,
        "password": hash_password(user_data.password),
        "nom": user_data.nom,
        "prenom": user_data.prenom,
        "role": "visiteur",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "must_set_password": False
    }
    
    await db.users.insert_one(user)
    
    token = generate_token()
    active_tokens[token] = user_id
    
    return {
        "token": token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "nom": user["nom"],
            "prenom": user["prenom"],
            "role": user["role"]
        }
    }

@api_router.post("/auth/login")
async def login(credentials: UserLogin):
    user = await db.users.find_one({
        "email": credentials.email,
        "password": hash_password(credentials.password)
    }, {"_id": 0})
    
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    token = generate_token()
    active_tokens[token] = user["id"]
    
    response_user = {
        "id": user["id"],
        "email": user["email"],
        "nom": user["nom"],
        "prenom": user["prenom"],
        "role": user["role"],
        "must_set_password": user.get("must_set_password", False)
    }
    
    if user["role"] == "stagiaire":
        response_user["groupe_id"] = user.get("groupe_id")
    
    return {"token": token, "user": response_user}

@api_router.post("/auth/set-password")
async def set_password(token: str, new_password: str):
    """Set password for users who must set their password (formateurs created by admin)"""
    user = await get_current_user(token)
    
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Le mot de passe doit contenir au moins 6 caractères")
    
    await db.users.update_one(
        {"id": user["id"]},
        {"$set": {"password": hash_password(new_password), "must_set_password": False}}
    )
    
    return {"message": "Mot de passe mis à jour avec succès"}

@api_router.get("/auth/me")
async def get_me(token: str):
    user = await get_current_user(token)
    response = {
        "id": user["id"],
        "email": user["email"],
        "nom": user["nom"],
        "prenom": user["prenom"],
        "role": user["role"],
        "must_set_password": user.get("must_set_password", False)
    }
    if user["role"] == "stagiaire":
        response["groupe_id"] = user.get("groupe_id")
    return response

@api_router.post("/auth/logout")
async def logout(token: str):
    if token in active_tokens:
        del active_tokens[token]
    return {"message": "Déconnexion réussie"}

# ============== ADMIN ROUTES ==============

@api_router.post("/admin/formateur")
async def create_formateur(data: AdminCreateFormateur, token: str):
    """Admin creates a new formateur account"""
    await require_admin(token)
    
    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")
    
    # Generate temporary password
    temp_password = secrets.token_urlsafe(12)
    
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": data.email,
        "password": hash_password(temp_password),
        "nom": data.nom,
        "prenom": data.prenom,
        "role": "formateur",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "must_set_password": True
    }
    
    await db.users.insert_one(user)
    
    return {
        "message": "Formateur créé avec succès",
        "formateur": {
            "id": user["id"],
            "email": user["email"],
            "nom": user["nom"],
            "prenom": user["prenom"]
        },
        "temp_password": temp_password
    }

@api_router.delete("/admin/formateur/{formateur_id}")
async def delete_formateur(formateur_id: str, token: str):
    """Admin deletes a formateur account"""
    await require_admin(token)
    
    formateur = await db.users.find_one({"id": formateur_id, "role": "formateur"}, {"_id": 0})
    if not formateur:
        raise HTTPException(status_code=404, detail="Formateur non trouvé")
    
    # Delete formateur
    await db.users.delete_one({"id": formateur_id})
    
    # Deactivate their groups
    await db.groupes_formation.update_many(
        {"formateur_id": formateur_id},
        {"$set": {"is_active": False}}
    )
    
    return {"message": "Formateur supprimé avec succès"}

@api_router.get("/admin/formateurs")
async def get_all_formateurs(token: str):
    """Admin gets all formateurs"""
    await require_admin(token)
    
    # Optimized: Use aggregation to get formateurs with group counts in single query
    pipeline = [
        {"$match": {"role": "formateur"}},
        {"$lookup": {
            "from": "groupes_formation",
            "localField": "id",
            "foreignField": "formateur_id",
            "as": "groupes"
        }},
        {"$addFields": {"nb_groupes": {"$size": "$groupes"}}},
        {"$project": {"groupes": 0, "password": 0, "_id": 0}}
    ]
    formateurs = await db.users.aggregate(pipeline).to_list(1000)
    
    return formateurs

@api_router.post("/admin/quiz")
async def admin_create_quiz(data: QuizCreate, token: str):
    """Admin creates a new quiz"""
    await require_admin(token)
    
    # Verify chapter exists
    chapter = await db.chapters.find_one({"id": data.chapter_id}, {"_id": 0})
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapitre non trouvé")
    
    quiz_id = str(uuid.uuid4())
    questions = []
    for i, q in enumerate(data.questions):
        questions.append({
            "id": f"q-{quiz_id}-{i}",
            "question": q.question,
            "type": q.type,
            "options": q.options,
            "correct_answer": q.correct_answer,
            "explication": q.explication
        })
    
    quiz = {
        "id": quiz_id,
        "chapter_id": data.chapter_id,
        "titre": data.titre,
        "video_url": data.video_url,
        "questions": questions,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.quizzes.insert_one(quiz)
    
    return {"message": "Quiz créé avec succès", "quiz_id": quiz_id}

@api_router.put("/admin/quiz/{quiz_id}")
async def admin_update_quiz(quiz_id: str, data: QuizUpdate, token: str):
    """Admin updates a quiz"""
    await require_admin(token)
    
    quiz = await db.quizzes.find_one({"id": quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz non trouvé")
    
    update_data = {}
    if data.titre is not None:
        update_data["titre"] = data.titre
    if data.video_url is not None:
        update_data["video_url"] = data.video_url
    if data.questions is not None:
        questions = []
        for i, q in enumerate(data.questions):
            questions.append({
                "id": f"q-{quiz_id}-{i}",
                "question": q.question,
                "type": q.type,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "explication": q.explication
            })
        update_data["questions"] = questions
    
    if update_data:
        await db.quizzes.update_one({"id": quiz_id}, {"$set": update_data})
    
    return {"message": "Quiz mis à jour avec succès"}

@api_router.delete("/admin/quiz/{quiz_id}")
async def admin_delete_quiz(quiz_id: str, token: str):
    """Admin deletes a quiz"""
    await require_admin(token)
    
    result = await db.quizzes.delete_one({"id": quiz_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Quiz non trouvé")
    
    return {"message": "Quiz supprimé avec succès"}

# ============== ADMIN CHAPTER MANAGEMENT ==============

@api_router.post("/admin/chapter")
async def admin_create_chapter(data: dict, token: str):
    """Admin creates a new chapter"""
    await require_admin(token)
    
    # Generate chapter ID
    chapter_id = f"{data['formation_type'].lower()}1-ch{data['numero']}" if data['formation_type'] == 'PSC' else f"ch{data['numero']}"
    
    chapter = {
        "id": chapter_id,
        "numero": data['numero'],
        "titre": data['titre'],
        "description": data.get('description', ''),
        "icon": data.get('icon', 'BookOpen'),
        "formation_type": data['formation_type'],
        "image_url": data.get('image_url', ''),
        "fiches": data.get('fiches', [])
    }
    
    await db.chapters.insert_one(chapter)
    
    # Remove _id before returning (MongoDB adds it)
    if '_id' in chapter:
        del chapter['_id']
    
    return chapter

@api_router.put("/admin/chapter/{chapter_id}")
async def admin_update_chapter(chapter_id: str, data: dict, token: str):
    """Admin updates a chapter"""
    await require_admin(token)
    
    # Remove _id if present
    if '_id' in data:
        del data['_id']
    
    result = await db.chapters.update_one(
        {"id": chapter_id},
        {"$set": data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Chapitre non trouvé")
    
    updated_chapter = await db.chapters.find_one({"id": chapter_id}, {"_id": 0})
    return updated_chapter

@api_router.delete("/admin/chapter/{chapter_id}")
async def admin_delete_chapter(chapter_id: str, token: str):
    """Admin deletes a chapter"""
    await require_admin(token)
    
    # Also delete associated quizzes
    await db.quizzes.delete_many({"chapter_id": chapter_id})
    
    result = await db.chapters.delete_one({"id": chapter_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Chapitre non trouvé")
    
    return {"message": "Chapitre et quiz associés supprimés avec succès"}


@api_router.get("/admin/stats")
async def admin_get_stats(token: str):
    """Admin gets global statistics"""
    await require_admin(token)
    
    total_formateurs = await db.users.count_documents({"role": "formateur"})
    total_stagiaires = await db.users.count_documents({"role": "stagiaire"})
    total_visiteurs = await db.users.count_documents({"role": "visiteur"})
    total_groupes = await db.groupes_formation.count_documents({})
    total_quizzes = await db.quizzes.count_documents({})
    total_quiz_results = await db.quiz_results.count_documents({})
    
    return {
        "total_formateurs": total_formateurs,
        "total_stagiaires": total_stagiaires,
        "total_visiteurs": total_visiteurs,
        "total_groupes": total_groupes,
        "total_quizzes": total_quizzes,
        "total_quiz_completés": total_quiz_results
    }

# ============== FORMATEUR ROUTES ==============

@api_router.post("/formateur/groupe")
async def create_groupe(data: GroupeFormationCreate, token: str):
    """Formateur creates a new training group"""
    user = await require_formateur(token)
    
    if data.seuil_reussite < 80:
        raise HTTPException(status_code=400, detail="Le seuil de réussite ne peut pas être inférieur à 80%")
    
    groupe_id = str(uuid.uuid4())
    code_acces = generate_code_groupe()
    
    # Make sure code is unique
    while await db.groupes_formation.find_one({"code_acces": code_acces}):
        code_acces = generate_code_groupe()
    
    groupe = {
        "id": groupe_id,
        "nom": data.nom,
        "code_acces": code_acces,
        "formateur_id": user["id"],
        "formation_type": data.formation_type,
        "seuil_reussite": data.seuil_reussite,
        "chapitres_ordre": data.chapitres_ordre,
        "collaborateurs": [],
        "max_stagiaires": 18,
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.groupes_formation.insert_one(groupe)
    
    return {
        "message": "Groupe créé avec succès",
        "groupe": {
            "id": groupe["id"],
            "nom": groupe["nom"],
            "code_acces": groupe["code_acces"],
            "formation_type": groupe["formation_type"]
        }
    }

@api_router.get("/formateur/groupes")
async def get_formateur_groupes(token: str):
    """Get all groups for a formateur (owned + collaborated)"""
    user = await require_formateur(token)
    
    # Groups owned by formateur or where they are collaborator
    groupes = await db.groupes_formation.find({
        "$or": [
            {"formateur_id": user["id"]},
            {"collaborateurs": user["id"]}
        ]
    }, {"_id": 0}).to_list(1000)
    
    # Add stagiaire count for each group
    for groupe in groupes:
        groupe["nb_stagiaires"] = await db.users.count_documents({"groupe_id": groupe["id"]})
    
    return groupes

@api_router.get("/formateur/groupe/{groupe_id}")
async def get_groupe_detail(groupe_id: str, token: str):
    """Get detailed info about a group"""
    user = await require_formateur(token)
    
    groupe = await db.groupes_formation.find_one({"id": groupe_id}, {"_id": 0})
    if not groupe:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    # Check access
    if groupe["formateur_id"] != user["id"] and user["id"] not in groupe["collaborateurs"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Vous n'avez pas accès à ce groupe")
    
    groupe["nb_stagiaires"] = await db.users.count_documents({"groupe_id": groupe_id})
    
    # Get stagiaires list with only required fields
    stagiaires = await db.users.find(
        {"groupe_id": groupe_id}, 
        {"_id": 0, "password": 0, "id": 1, "nom": 1, "prenom": 1, "email": 1, "created_at": 1, "role": 1, "groupe_id": 1}
    ).to_list(100)
    
    # Optimized: Batch fetch all progress and quiz stats in 2 queries instead of N+1
    user_ids = [s["id"] for s in stagiaires]
    
    # Batch fetch progress
    all_progress_list = await db.stagiaire_progress.find(
        {"user_id": {"$in": user_ids}}, 
        {"_id": 0}
    ).to_list(100)
    all_progress = {p["user_id"]: p for p in all_progress_list}
    
    # Batch fetch quiz stats using aggregation
    quiz_stats_pipeline = [
        {"$match": {"user_id": {"$in": user_ids}}},
        {"$group": {
            "_id": "$user_id",
            "count": {"$sum": 1},
            "avg_score": {"$avg": "$percentage"}
        }}
    ]
    quiz_stats_list = await db.quiz_results.aggregate(quiz_stats_pipeline).to_list(100)
    quiz_stats = {qs["_id"]: qs for qs in quiz_stats_list}
    
    # Assign data to stagiaires
    for stagiaire in stagiaires:
        progress = all_progress.get(stagiaire["id"])
        if progress:
            stagiaire["chapitres_completes"] = len(progress.get("chapitres_completes", []))
            stagiaire["chapitres_debloques"] = len(progress.get("chapitres_debloques", []))
        else:
            stagiaire["chapitres_completes"] = 0
            stagiaire["chapitres_debloques"] = 0
        
        qs = quiz_stats.get(stagiaire["id"])
        stagiaire["quizzes_completed"] = qs["count"] if qs else 0
        stagiaire["average_score"] = qs["avg_score"] if qs else 0
    
    return {"groupe": groupe, "stagiaires": stagiaires}

@api_router.put("/formateur/groupe/{groupe_id}")
async def update_groupe(groupe_id: str, data: GroupeFormationUpdate, token: str):
    """Update a training group"""
    user = await require_formateur(token)
    
    groupe = await db.groupes_formation.find_one({"id": groupe_id}, {"_id": 0})
    if not groupe:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    if groupe["formateur_id"] != user["id"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Seul le créateur du groupe peut le modifier")
    
    update_data = {}
    if data.nom is not None:
        update_data["nom"] = data.nom
    if data.seuil_reussite is not None:
        if data.seuil_reussite < 80:
            raise HTTPException(status_code=400, detail="Le seuil ne peut pas être inférieur à 80%")
        update_data["seuil_reussite"] = data.seuil_reussite
    if data.chapitres_ordre is not None:
        update_data["chapitres_ordre"] = data.chapitres_ordre
    if data.is_active is not None:
        update_data["is_active"] = data.is_active
    
    if update_data:
        await db.groupes_formation.update_one({"id": groupe_id}, {"$set": update_data})
    
    return {"message": "Groupe mis à jour avec succès"}

@api_router.post("/formateur/groupe/{groupe_id}/invite")
async def invite_collaborator(groupe_id: str, data: CollaborationInvite, token: str):
    """Invite another formateur to collaborate on a group"""
    user = await require_formateur(token)
    
    groupe = await db.groupes_formation.find_one({"id": groupe_id}, {"_id": 0})
    if not groupe:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    if groupe["formateur_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Seul le créateur du groupe peut inviter des collaborateurs")
    
    # Find formateur to invite
    formateur = await db.users.find_one({"email": data.formateur_email, "role": "formateur"}, {"_id": 0})
    if not formateur:
        raise HTTPException(status_code=404, detail="Formateur non trouvé")
    
    if formateur["id"] in groupe["collaborateurs"]:
        raise HTTPException(status_code=400, detail="Ce formateur est déjà collaborateur")
    
    await db.groupes_formation.update_one(
        {"id": groupe_id},
        {"$push": {"collaborateurs": formateur["id"]}}
    )
    
    return {"message": f"{formateur['prenom']} {formateur['nom']} a été ajouté comme collaborateur"}

@api_router.delete("/formateur/groupe/{groupe_id}/collaborateur/{collaborateur_id}")
async def remove_collaborator(groupe_id: str, collaborateur_id: str, token: str):
    """Remove a collaborator from a group"""
    user = await require_formateur(token)
    
    groupe = await db.groupes_formation.find_one({"id": groupe_id}, {"_id": 0})
    if not groupe:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    if groupe["formateur_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Seul le créateur du groupe peut retirer des collaborateurs")
    
    await db.groupes_formation.update_one(
        {"id": groupe_id},
        {"$pull": {"collaborateurs": collaborateur_id}}
    )
    
    return {"message": "Collaborateur retiré avec succès"}

@api_router.get("/formateur/stagiaire/{stagiaire_id}")
async def get_stagiaire_detail(stagiaire_id: str, token: str):
    """Get detailed progress of a stagiaire"""
    user = await require_formateur(token)
    
    stagiaire = await db.users.find_one({"id": stagiaire_id, "role": "stagiaire"}, {"_id": 0, "password": 0})
    if not stagiaire:
        raise HTTPException(status_code=404, detail="Stagiaire non trouvé")
    
    # Check if formateur has access to this stagiaire
    groupe = await db.groupes_formation.find_one({"id": stagiaire.get("groupe_id")}, {"_id": 0})
    if not groupe:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    if groupe["formateur_id"] != user["id"] and user["id"] not in groupe["collaborateurs"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Vous n'avez pas accès à ce stagiaire")
    
    # Get progress
    progress = await db.stagiaire_progress.find_one({"user_id": stagiaire_id}, {"_id": 0})
    
    # Get quiz results
    results = await db.quiz_results.find({"user_id": stagiaire_id}, {"_id": 0}).sort("completed_at", -1).to_list(1000)
    
    return {
        "stagiaire": stagiaire,
        "groupe": groupe,
        "progress": progress,
        "quiz_results": results
    }

# ============== CHAPTERS ROUTES ==============

@api_router.get("/chapters")
async def get_chapters(formation_type: str = "PSE", token: Optional[str] = None):
    """Get chapters - filtered by formation type"""
    chapters = await db.chapters.find({"formation_type": formation_type}, {"_id": 0}).sort("numero", 1).to_list(100)
    return chapters

@api_router.get("/chapters/preview")
async def get_chapters_preview():
    """Get preview chapters for free visitors (first 3 chapters, limited fiches)"""
    chapters = await db.chapters.find({"formation_type": "PSE"}, {"_id": 0}).sort("numero", 1).to_list(3)
    
    # Limit fiches to first one only
    for chapter in chapters:
        if chapter.get("fiches"):
            chapter["fiches"] = [chapter["fiches"][0]] if chapter["fiches"] else []
            chapter["is_preview"] = True
    
    return chapters

@api_router.get("/chapters/{chapter_id}")
async def get_chapter(chapter_id: str, token: Optional[str] = None):
    chapter = await db.chapters.find_one({"id": chapter_id}, {"_id": 0})
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapitre non trouvé")
    return chapter

# ============== STAGIAIRE ROUTES ==============

@api_router.get("/stagiaire/progress")
async def get_stagiaire_progress(token: str):
    """Get current stagiaire's progress"""
    user = await get_current_user(token)
    
    if user["role"] != "stagiaire":
        raise HTTPException(status_code=403, detail="Accès réservé aux stagiaires")
    
    progress = await db.stagiaire_progress.find_one({"user_id": user["id"]}, {"_id": 0})
    if not progress:
        raise HTTPException(status_code=404, detail="Progression non trouvée")
    
    # Get groupe info
    groupe = await db.groupes_formation.find_one({"id": user.get("groupe_id")}, {"_id": 0})
    
    # Get quiz results
    results = await db.quiz_results.find({"user_id": user["id"]}, {"_id": 0}).to_list(1000)
    
    return {
        "progress": progress,
        "groupe": groupe,
        "quizzes_completed": len(results),
        "average_score": sum([r["percentage"] for r in results]) / len(results) if results else 0,
        "quiz_results": results
    }

@api_router.get("/stagiaire/chapitres")
async def get_stagiaire_chapitres(token: str):
    """Get chapters accessible to stagiaire based on their group progression"""
    user = await get_current_user(token)
    
    if user["role"] != "stagiaire":
        raise HTTPException(status_code=403, detail="Accès réservé aux stagiaires")
    
    progress = await db.stagiaire_progress.find_one({"user_id": user["id"]}, {"_id": 0})
    groupe = await db.groupes_formation.find_one({"id": user.get("groupe_id")}, {"_id": 0})
    
    if not progress or not groupe:
        raise HTTPException(status_code=404, detail="Données non trouvées")
    
    # Get all chapters in order defined by formateur
    all_chapters = await db.chapters.find({"formation_type": groupe["formation_type"]}, {"_id": 0}).to_list(100)
    
    # Create a map for quick lookup
    chapters_map = {ch["id"]: ch for ch in all_chapters}
    
    # Build response with unlock status
    result = []
    for ch_id in groupe["chapitres_ordre"]:
        if ch_id in chapters_map:
            chapter = chapters_map[ch_id]
            chapter["is_unlocked"] = ch_id in progress.get("chapitres_debloques", [])
            chapter["is_completed"] = ch_id in progress.get("chapitres_completes", [])
            result.append(chapter)
    
    return {"chapitres": result, "seuil_reussite": groupe["seuil_reussite"]}

# ============== QUIZ ROUTES ==============

@api_router.get("/quizzes")
async def get_quizzes():
    quizzes = await db.quizzes.find({}, {"_id": 0}).to_list(100)
    return quizzes

@api_router.get("/quizzes/{quiz_id}")
async def get_quiz_by_id(quiz_id: str):
    quiz = await db.quizzes.find_one({"id": quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz non trouvé")
    return quiz

@api_router.get("/quizzes/chapter/{chapter_id}")
async def get_quiz_by_chapter(chapter_id: str):
    quiz = await db.quizzes.find_one({"chapter_id": chapter_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz non trouvé pour ce chapitre")
    return quiz

@api_router.post("/quizzes/submit")
async def submit_quiz(submission: QuizSubmission, token: str):
    user = await get_current_user(token)
    
    quiz = await db.quizzes.find_one({"id": submission.quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz non trouvé")
    
    # Calculate score
    correct = 0
    answers_detail = []
    for i, answer in enumerate(submission.answers):
        if i < len(quiz["questions"]):
            question = quiz["questions"][i]
            is_correct = answer == question["correct_answer"]
            if is_correct:
                correct += 1
            answers_detail.append({
                "question_id": question["id"],
                "user_answer": answer,
                "correct_answer": question["correct_answer"],
                "is_correct": is_correct
            })
    
    total = len(quiz["questions"])
    percentage = (correct / total * 100) if total > 0 else 0
    
    result = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "quiz_id": submission.quiz_id,
        "chapter_id": quiz["chapter_id"],
        "score": correct,
        "total": total,
        "percentage": round(percentage, 1),
        "answers": answers_detail,
        "completed_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.quiz_results.insert_one(result)
    
    # Remove _id before returning
    if "_id" in result:
        del result["_id"]
    
    # For stagiaires, update progression if score >= seuil
    if user["role"] == "stagiaire":
        groupe = await db.groupes_formation.find_one({"id": user.get("groupe_id")}, {"_id": 0})
        if groupe and percentage >= groupe["seuil_reussite"]:
            progress = await db.stagiaire_progress.find_one({"user_id": user["id"]}, {"_id": 0})
            if progress:
                # Mark chapter as completed
                was_completed_before = quiz["chapter_id"] in progress.get("chapitres_completes", [])
                if not was_completed_before:
                    await db.stagiaire_progress.update_one(
                        {"user_id": user["id"]},
                        {"$addToSet": {"chapitres_completes": quiz["chapter_id"]}}
                    )
                
                # Unlock next chapter
                chapitres_ordre = groupe.get("chapitres_ordre", [])
                if quiz["chapter_id"] in chapitres_ordre:
                    current_idx = chapitres_ordre.index(quiz["chapter_id"])
                    if current_idx + 1 < len(chapitres_ordre):
                        next_chapter = chapitres_ordre[current_idx + 1]
                        await db.stagiaire_progress.update_one(
                            {"user_id": user["id"]},
                            {"$addToSet": {"chapitres_debloques": next_chapter}}
                        )
                        result["next_chapter_unlocked"] = next_chapter
                
                # Check if certificate is now earned (after this completion)
                if not was_completed_before:
                    updated_progress = await db.stagiaire_progress.find_one({"user_id": user["id"]}, {"_id": 0})
                    completed_chapters = updated_progress.get("chapitres_completes", [])
                    
                    # Get certificate config
                    config = await db.certificate_configs.find_one({"groupe_id": groupe["id"]}, {"_id": 0})
                    required_chapters = config["chapitres_obligatoires"] if config else groupe.get("chapitres_ordre", [])
                    
                    # Check if all required chapters are now completed
                    all_completed = all(ch in completed_chapters for ch in required_chapters)
                    
                    if all_completed and len(required_chapters) > 0:
                        result["certificate_earned"] = True
                        
                        # Send email notification to formateur
                        formateur = await db.users.find_one({"id": groupe["formateur_id"]}, {"_id": 0})
                        if formateur and formateur.get("email"):
                            stagiaire_name = f"{user['prenom']} {user['nom']}"
                            asyncio.create_task(
                                send_certificate_notification(
                                    formateur["email"],
                                    stagiaire_name,
                                    groupe["formation_type"],
                                    groupe["nom"]
                                )
                            )
    
    return result

@api_router.get("/quiz-results")
async def get_user_quiz_results(token: str):
    user = await get_current_user(token)
    results = await db.quiz_results.find({"user_id": user["id"]}, {"_id": 0}).sort("completed_at", -1).to_list(100)
    return results

# ============== CERTIFICATE ROUTES ==============

class CertificateConfig(BaseModel):
    chapitres_obligatoires: List[str]  # List of chapter IDs required for certificate

@api_router.get("/certificates/config/{groupe_id}")
async def get_certificate_config(groupe_id: str, token: str):
    """Get certificate configuration for a group"""
    user = await get_current_user(token)
    
    if user["role"] not in ["admin", "formateur"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    config = await db.certificate_configs.find_one({"groupe_id": groupe_id}, {"_id": 0})
    if not config:
        # Return default (all chapters required)
        groupe = await db.groupes_formation.find_one({"id": groupe_id}, {"_id": 0})
        if groupe:
            return {"groupe_id": groupe_id, "chapitres_obligatoires": groupe.get("chapitres_ordre", [])}
        return {"groupe_id": groupe_id, "chapitres_obligatoires": []}
    return config

@api_router.post("/certificates/config/{groupe_id}")
async def set_certificate_config(groupe_id: str, config: CertificateConfig, token: str):
    """Set certificate configuration for a group"""
    user = await get_current_user(token)
    
    if user["role"] not in ["admin", "formateur"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Verify group exists and user has access
    groupe = await db.groupes_formation.find_one({"id": groupe_id}, {"_id": 0})
    if not groupe:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
    
    if user["role"] == "formateur" and groupe["formateur_id"] != user["id"] and user["id"] not in groupe.get("collaborateurs", []):
        raise HTTPException(status_code=403, detail="Vous n'avez pas accès à ce groupe")
    
    await db.certificate_configs.update_one(
        {"groupe_id": groupe_id},
        {"$set": {"groupe_id": groupe_id, "chapitres_obligatoires": config.chapitres_obligatoires}},
        upsert=True
    )
    
    return {"message": "Configuration enregistrée", "chapitres_obligatoires": config.chapitres_obligatoires}

@api_router.get("/stagiaire/certificate/status")
async def get_certificate_status(token: str):
    """Check if stagiaire has earned their certificate"""
    user = await get_current_user(token)
    
    if user["role"] != "stagiaire":
        raise HTTPException(status_code=403, detail="Accès réservé aux stagiaires")
    
    progress = await db.stagiaire_progress.find_one({"user_id": user["id"]}, {"_id": 0})
    groupe = await db.groupes_formation.find_one({"id": user.get("groupe_id")}, {"_id": 0})
    
    if not progress or not groupe:
        return {"earned": False, "message": "Données non trouvées"}
    
    # Get certificate config
    config = await db.certificate_configs.find_one({"groupe_id": groupe["id"]}, {"_id": 0})
    required_chapters = config["chapitres_obligatoires"] if config else groupe.get("chapitres_ordre", [])
    
    # Check if all required chapters are completed
    completed = progress.get("chapitres_completes", [])
    all_completed = all(ch in completed for ch in required_chapters)
    
    return {
        "earned": all_completed,
        "required_chapters": required_chapters,
        "completed_chapters": completed,
        "remaining": [ch for ch in required_chapters if ch not in completed],
        "formation_type": groupe["formation_type"],
        "groupe_nom": groupe["nom"],
        "user_nom": f"{user['prenom']} {user['nom']}"
    }

@api_router.get("/stagiaire/certificate/generate")
async def generate_certificate(token: str):
    """Generate certificate PDF data for download"""
    user = await get_current_user(token)
    
    if user["role"] != "stagiaire":
        raise HTTPException(status_code=403, detail="Accès réservé aux stagiaires")
    
    # Check if certificate is earned
    progress = await db.stagiaire_progress.find_one({"user_id": user["id"]}, {"_id": 0})
    groupe = await db.groupes_formation.find_one({"id": user.get("groupe_id")}, {"_id": 0})
    
    if not progress or not groupe:
        raise HTTPException(status_code=404, detail="Données non trouvées")
    
    config = await db.certificate_configs.find_one({"groupe_id": groupe["id"]}, {"_id": 0})
    required_chapters = config["chapitres_obligatoires"] if config else groupe.get("chapitres_ordre", [])
    completed = progress.get("chapitres_completes", [])
    
    if not all(ch in completed for ch in required_chapters):
        raise HTTPException(status_code=400, detail="Certificat non disponible - formation incomplète")
    
    # Get quiz results for average score
    results = await db.quiz_results.find({"user_id": user["id"]}, {"_id": 0}).to_list(1000)
    average_score = sum([r["percentage"] for r in results]) / len(results) if results else 0
    
    return {
        "certificate_data": {
            "nom": user["nom"],
            "prenom": user["prenom"],
            "email": user["email"],
            "formation_type": groupe["formation_type"],
            "groupe_nom": groupe["nom"],
            "completion_date": datetime.now(timezone.utc).isoformat(),
            "average_score": round(average_score, 1),
            "chapters_completed": len(completed),
            "certificate_title": f"Certificat de validation de la FOAD {groupe['formation_type']} 1"
        }
    }

@api_router.get("/stagiaire/certificate/pdf")
async def generate_certificate_pdf(token: str):
    """Generate certificate PDF file for download"""
    user = await get_current_user(token)
    
    if user["role"] != "stagiaire":
        raise HTTPException(status_code=403, detail="Accès réservé aux stagiaires")
    
    # Check if certificate is earned
    progress = await db.stagiaire_progress.find_one({"user_id": user["id"]}, {"_id": 0})
    groupe = await db.groupes_formation.find_one({"id": user.get("groupe_id")}, {"_id": 0})
    
    if not progress or not groupe:
        raise HTTPException(status_code=404, detail="Données non trouvées")
    
    config = await db.certificate_configs.find_one({"groupe_id": groupe["id"]}, {"_id": 0})
    required_chapters = config["chapitres_obligatoires"] if config else groupe.get("chapitres_ordre", [])
    completed = progress.get("chapitres_completes", [])
    
    if not all(ch in completed for ch in required_chapters):
        raise HTTPException(status_code=400, detail="Certificat non disponible - formation incomplète")
    
    # Get quiz results for average score
    results = await db.quiz_results.find({"user_id": user["id"]}, {"_id": 0}).to_list(1000)
    average_score = sum([r["percentage"] for r in results]) / len(results) if results else 0
    
    # Generate PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CertTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#dc2626'),
        alignment=TA_CENTER,
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'CertSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    name_style = ParagraphStyle(
        'CertName',
        parent=styles['Heading1'],
        fontSize=36,
        textColor=colors.HexColor('#1e293b'),
        alignment=TA_CENTER,
        spaceBefore=20,
        spaceAfter=20
    )
    
    body_style = ParagraphStyle(
        'CertBody',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#475569'),
        alignment=TA_CENTER,
        spaceAfter=10
    )
    
    score_style = ParagraphStyle(
        'CertScore',
        parent=styles['Heading2'],
        fontSize=24,
        textColor=colors.HexColor('#059669'),
        alignment=TA_CENTER,
        spaceBefore=15,
        spaceAfter=15
    )
    
    footer_style = ParagraphStyle(
        'CertFooter',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#94a3b8'),
        alignment=TA_CENTER,
        spaceBefore=30
    )
    
    # Build certificate content
    story = []
    
    # Add logo if exists
    logo_path = Path("/app/frontend/public/images/logo-secours73.png")
    if logo_path.exists():
        img = Image(str(logo_path), width=3*cm, height=3*cm)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 0.5*cm))
    
    # Title
    story.append(Paragraph("CERTIFICAT DE VALIDATION", title_style))
    story.append(Paragraph(f"Formation Ouverte à Distance - {groupe['formation_type']} 1", subtitle_style))
    
    # Certifies text
    story.append(Paragraph("Nous certifions que", body_style))
    
    # Name
    story.append(Paragraph(f"{user['prenom']} {user['nom']}", name_style))
    
    # Achievement
    story.append(Paragraph(
        f"a validé avec succès l'ensemble des modules de la<br/>"
        f"<font color='#dc2626'><b>Formation Ouverte à Distance Premiers Secours en Équipe - {groupe['formation_type']}</b></font>",
        body_style
    ))
    
    # Score
    story.append(Paragraph(f"Score moyen: {round(average_score, 1)}%", score_style))
    
    # Details
    story.append(Paragraph(
        f"Groupe de formation: <b>{groupe['nom']}</b><br/>"
        f"{len(completed)} chapitres complétés",
        body_style
    ))
    
    # Date
    completion_date = datetime.now(timezone.utc).strftime("%d %B %Y")
    story.append(Paragraph(f"Délivré le {completion_date}", body_style))
    
    # Footer
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "Secours Alpes 73 - Association agréée pour la formation aux premiers secours<br/>"
        "Ce certificat atteste de la validation de la partie théorique de la formation",
        footer_style
    ))
    
    doc.build(story)
    buffer.seek(0)
    
    filename = f"certificat_FOAD_{groupe['formation_type']}_{user['nom']}_{user['prenom']}.pdf"
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ============== EMAIL NOTIFICATIONS ==============

async def send_certificate_notification(formateur_email: str, stagiaire_name: str, formation_type: str, groupe_nom: str):
    """Send email notification to formateur when stagiaire earns certificate"""
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #dc2626;">Secours Alpes 73</h1>
        </div>
        
        <div style="background-color: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
            <h2 style="color: #166534; margin: 0 0 10px 0;">🎉 Félicitations !</h2>
            <p style="color: #15803d; margin: 0; font-size: 18px;">
                <strong>{stagiaire_name}</strong> a validé la FOAD {formation_type} 1
            </p>
        </div>
        
        <p style="color: #475569;">
            Un stagiaire de votre groupe <strong>{groupe_nom}</strong> vient de compléter avec succès 
            tous les chapitres requis pour obtenir son certificat de validation.
        </p>
        
        <p style="color: #475569;">
            Vous pouvez consulter les détails de sa progression sur votre espace formateur.
        </p>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center;">
            <p style="color: #94a3b8; font-size: 12px;">
                Secours Alpes 73 - Plateforme de Formation aux Premiers Secours
            </p>
        </div>
    </div>
    """
    
    return await send_email(
        formateur_email,
        f"🎓 {stagiaire_name} a validé la FOAD {formation_type} 1",
        html_content
    )

# ============== VIDEO UPLOAD ==============

@api_router.post("/upload/video")
async def upload_video(file: UploadFile = File(...), token: str = Query(...)):
    """Upload a video file"""
    user = await get_current_user(token)
    
    if user["role"] not in ["admin", "formateur"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    # Validate file type
    allowed_types = ["video/mp4", "video/webm", "video/ogg", "video/quicktime"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Type de fichier non autorisé. Utilisez MP4, WebM, OGG ou MOV.")
    
    # Validate file size (max 100MB)
    max_size = 100 * 1024 * 1024  # 100MB
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(status_code=400, detail="Fichier trop volumineux. Maximum 100MB.")
    
    # Generate unique filename
    ext = Path(file.filename).suffix or ".mp4"
    video_id = str(uuid.uuid4())
    filename = f"{video_id}{ext}"
    filepath = VIDEO_UPLOAD_DIR / filename
    
    # Save file
    with open(filepath, "wb") as f:
        f.write(content)
    
    # Store metadata in database
    video_doc = {
        "id": video_id,
        "filename": filename,
        "original_name": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "uploaded_by": user["id"],
        "uploaded_at": datetime.now(timezone.utc).isoformat()
    }
    await db.videos.insert_one(video_doc)
    
    return {
        "id": video_id,
        "filename": filename,
        "url": f"/api/videos/{video_id}",
        "size": len(content)
    }

@api_router.get("/videos/{video_id}")
async def get_video(video_id: str):
    """Stream a video file"""
    video = await db.videos.find_one({"id": video_id}, {"_id": 0})
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")
    
    filepath = VIDEO_UPLOAD_DIR / video["filename"]
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Fichier vidéo non trouvé")
    
    return FileResponse(
        filepath,
        media_type=video.get("content_type", "video/mp4"),
        filename=video.get("original_name", video["filename"])
    )

@api_router.delete("/videos/{video_id}")
async def delete_video(video_id: str, token: str):
    """Delete a video file"""
    user = await get_current_user(token)
    
    if user["role"] not in ["admin", "formateur"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé")
    
    video = await db.videos.find_one({"id": video_id}, {"_id": 0})
    if not video:
        raise HTTPException(status_code=404, detail="Vidéo non trouvée")
    
    # Delete file
    filepath = VIDEO_UPLOAD_DIR / video["filename"]
    if filepath.exists():
        filepath.unlink()
    
    # Delete from database
    await db.videos.delete_one({"id": video_id})
    
    return {"message": "Vidéo supprimée avec succès"}

# ============== PSC ROUTES (Placeholder) ==============

@api_router.get("/psc/chapters")
async def get_psc_chapters():
    """Get PSC chapters - free unlimited access"""
    chapters = await db.chapters.find({"formation_type": "PSC"}, {"_id": 0}).sort("numero", 1).to_list(100)
    return chapters

# ============== BNSSA ROUTES (Placeholder) ==============

@api_router.get("/bnssa/chapters")
async def get_bnssa_chapters(token: str):
    """Get BNSSA chapters - requires stagiaire authorization"""
    user = await get_current_user(token)
    
    if user["role"] == "visiteur":
        raise HTTPException(status_code=403, detail="Accès non autorisé pour les visiteurs")
    
    if user["role"] == "stagiaire":
        groupe = await db.groupes_formation.find_one({"id": user.get("groupe_id")}, {"_id": 0})
        if not groupe or groupe.get("formation_type") != "BNSSA":
            raise HTTPException(status_code=403, detail="Votre groupe n'a pas accès à la formation BNSSA")
    
    chapters = await db.chapters.find({"formation_type": "BNSSA"}, {"_id": 0}).sort("numero", 1).to_list(100)
    return chapters

# ============== SEED DATA ==============

@api_router.post("/seed")
async def seed_database():
    # Check if already seeded using a specific flag
    seed_flag = await db.system_flags.find_one({"flag": "database_seeded"})
    if seed_flag:
        # Return existing stats
        users_count = await db.users.count_documents({})
        chapters_count = await db.chapters.count_documents({})
        quizzes_count = await db.quizzes.count_documents({})
        return {
            "message": "Base de données déjà initialisée",
            "users": users_count,
            "chapters": chapters_count,
            "quizzes": quizzes_count,
            "seeded_at": seed_flag.get("created_at", "unknown")
        }
    
    # Clear any existing data to ensure clean seed
    await db.users.delete_many({})
    await db.chapters.delete_many({})
    await db.quizzes.delete_many({})
    await db.groupes.delete_many({})
    
    # Create admin user
    admin_id = str(uuid.uuid4())
    admin = {
        "id": admin_id,
        "email": "ledisque.tanguy73@hotmail.com",
        "password": hash_password("NewAdmin123!"),
        "nom": "Ledisque",
        "prenom": "Tanguy",
        "role": "admin",
        "verified": True
    }
    await db.users.insert_one(admin)
    
    # Create test formateur
    formateur_id = str(uuid.uuid4())
    formateur = {
        "id": formateur_id,
        "email": "test@secours73.fr",
        "password": hash_password("test123"),
        "nom": "Test",
        "prenom": "Formateur",
        "role": "formateur",
        "verified": True
    }
    await db.users.insert_one(formateur)
    
    # Create test groupe
    groupe_id = str(uuid.uuid4())
    groupe = {
        "id": groupe_id,
        "nom": "Groupe Test",
        "code": "TEST0000",
        "seuil_validation": 0,
        "formateur_id": formateur_id,
        "chapitres_obligatoires": []
    }
    await db.groupes.insert_one(groupe)
    
    # Create test stagiaire
    stagiaire_id = str(uuid.uuid4())
    stagiaire = {
        "id": stagiaire_id,
        "email": "stagiaire.test@secours73.fr",
        "password": hash_password("test123"),
        "nom": "Test",
        "prenom": "Stagiaire",
        "role": "stagiaire",
        "groupe_id": groupe_id,
        "formation_type": "PSE",
        "verified": True
    }
    await db.users.insert_one(stagiaire)
    
    # Seed PSE chapters based on PSE PDF content
    chapters = [
        {
            "id": "ch1",
            "numero": 1,
            "titre": "Attitude et comportement du secouriste",
            "description": "Le rôle du citoyen secouriste, attitude professionnelle, abord relationnel de la victime, gestion du stress.",
            "icon": "Shield",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f1-1",
                    "titre": "Le citoyen de sécurité civile",
                    "contenu": "Le secouriste est un acteur essentiel de la chaîne des secours. Il intervient en premier sur les lieux d'un accident ou d'un malaise. Sa mission est de protéger, alerter et secourir en attendant l'arrivée des secours professionnels.\n\n**Protection juridique:**\nLe secouriste bénéficie d'une protection juridique lorsqu'il porte assistance à une personne en péril. L'article 122-7 du Code pénal précise que n'est pas pénalement responsable la personne qui accomplit un acte commandé par la nécessité de sauvegarder une personne d'un péril grave et imminent.\n\n**Principes fondamentaux:**\n- Agir dans la limite de ses compétences\n- Ne jamais se mettre en danger\n- Respecter la victime et sa dignité\n- Maintenir le secret professionnel"
                },
                {
                    "id": "f1-2",
                    "titre": "Attitude et comportement",
                    "contenu": "Le secouriste doit adopter une attitude professionnelle en toutes circonstances:\n\n**Qualités essentielles:**\n- **Organisation**: Anticiper et préparer son intervention\n- **Rigueur**: Suivre les protocoles établis\n- **Calme**: Garder son sang-froid face à l'urgence\n- **Humilité**: Reconnaître ses limites\n- **Discrétion**: Respecter la confidentialité\n\n**Communication avec la victime:**\n- Se présenter clairement\n- Expliquer ce que l'on fait\n- Rassurer sans mentir\n- Écouter activement"
                },
                {
                    "id": "f1-3",
                    "titre": "L'impact psychologique",
                    "contenu": "L'intervention sur une situation d'urgence peut avoir un impact psychologique sur le secouriste.\n\n**Réactions normales:**\n- Stress aigu pendant l'intervention\n- Fatigue après l'intervention\n- Besoin de parler de ce qu'on a vécu\n\n**Signes d'alerte:**\n- Troubles du sommeil persistants\n- Irritabilité inhabituelle\n- Flashbacks récurrents\n- Évitement des situations similaires\n\n**Préservation du potentiel mental:**\n- Participer aux débriefings\n- Ne pas rester isolé\n- Consulter si les symptômes persistent"
                }
            ]
        },
        {
            "id": "ch2",
            "numero": 2,
            "titre": "Bilans",
            "description": "Évaluation de la victime: les 4 regards, surveillance, transmission des informations, mesure des paramètres vitaux.",
            "icon": "ClipboardList",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f2-1",
                    "titre": "Les 4 regards",
                    "contenu": "L'évaluation de la victime s'effectue en 4 étapes appelées 'regards':\n\n**Premier regard - Observation générale:**\n- Identifier les dangers\n- Évaluer le mécanisme de l'accident\n- Compter le nombre de victimes\n\n**Deuxième regard - Menaces vitales:**\n- La victime saigne-t-elle abondamment?\n- La victime s'étouffe-t-elle?\n- La victime répond-elle?\n- La victime respire-t-elle?\n\n**Troisième regard - Fonctions vitales:**\n- Évaluer la fonction respiratoire\n- Évaluer la fonction circulatoire\n- Évaluer la fonction neurologique\n\n**Quatrième regard - Interrogatoire:**\n- Que s'est-il passé?\n- Où avez-vous mal?\n- Avez-vous des antécédents médicaux?\n- Prenez-vous des médicaments?"
                },
                {
                    "id": "f2-2",
                    "titre": "Paramètres vitaux",
                    "contenu": "**Fréquence respiratoire (FR):**\n- Adulte: 12 à 20 cycles/min\n- Enfant: 20 à 30 cycles/min\n- Nourrisson: 30 à 40 cycles/min\n\n**Saturation en oxygène (SpO2):**\n- Normale: 95 à 100%\n- Insuffisante: < 94%\n\n**Fréquence cardiaque (FC):**\n- Adulte: 60 à 100 bpm\n- Enfant: 70 à 140 bpm\n- Nourrisson: 100 à 160 bpm\n\n**Pression artérielle (PA):**\n- Normale: 120/80 mmHg environ\n- Hypotension: < 90 mmHg systolique\n- Hypertension: > 140/90 mmHg\n\n**Température:**\n- Normale: 36,5°C à 37,5°C\n- Hypothermie: < 35°C\n- Hyperthermie: > 38,5°C"
                },
                {
                    "id": "f2-3",
                    "titre": "Échelles d'évaluation",
                    "contenu": "**Score de Glasgow (conscience):**\nÉvalue 3 paramètres sur 15 points:\n- Ouverture des yeux (1-4)\n- Réponse verbale (1-5)\n- Réponse motrice (1-6)\n\n**Score EVDA:**\n- É: Éveillé (yeux ouverts spontanément)\n- V: réagit à la Voix\n- D: réagit à la Douleur\n- A: Aucune réaction\n\n**Score FAST (AVC):**\n- Face: asymétrie du visage\n- Arm: faiblesse d'un bras\n- Speech: troubles de la parole\n- Time: heure de début des symptômes\n\n**Évaluation de la douleur:**\n- Échelle numérique (0-10)\n- Échelle verbale (absente/faible/modérée/intense/très intense)"
                }
            ]
        },
        {
            "id": "ch3",
            "numero": 3,
            "titre": "Protection et sécurité",
            "description": "Équipements de protection, sécurité sur intervention, dégagement d'urgence.",
            "icon": "HardHat",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f3-1",
                    "titre": "Équipements de protection individuelle",
                    "contenu": "**EPI obligatoires:**\n- Gants à usage unique (latex, nitrile ou vinyle)\n- Masque de protection respiratoire\n- Lunettes de protection si risque de projection\n- Gilet haute visibilité (intervention routière)\n\n**Règles d'utilisation:**\n- Changer de gants entre chaque victime\n- Ne jamais toucher son visage avec des gants souillés\n- Éliminer les EPI usagés dans les conteneurs appropriés"
                },
                {
                    "id": "f3-2",
                    "titre": "Sécurité sur intervention",
                    "contenu": "**Identification des dangers:**\n- Circulation routière\n- Incendie / fumées\n- Électricité\n- Produits dangereux\n- Risque d'effondrement\n\n**Mesures de protection:**\n- Baliser la zone\n- Couper les sources de danger si possible\n- Éloigner les personnes non concernées\n- Demander des renforts si nécessaire\n\n**Ne jamais:**\n- Se mettre en danger pour secourir\n- Intervenir sans protection adaptée\n- Négliger un danger potentiel"
                },
                {
                    "id": "f3-3",
                    "titre": "Dégagement d'urgence",
                    "contenu": "Le dégagement d'urgence n'est réalisé que si la victime est exposée à un danger vital immédiat et non contrôlable.\n\n**Indications:**\n- Incendie\n- Risque d'explosion\n- Effondrement imminent\n- Noyade\n\n**Techniques:**\n- Traction par les chevilles\n- Traction par les poignets\n- Traction par les vêtements\n- Dégagement avec aide d'un tiers\n\n**Précautions:**\n- Maintenir l'axe tête-cou-tronc si traumatisme suspecté\n- Agir rapidement mais sans précipitation\n- Déplacer la victime vers un lieu sûr à proximité"
                }
            ]
        },
        {
            "id": "ch4",
            "numero": 4,
            "titre": "Hygiène et asepsie",
            "description": "Précautions standards, lavage des mains, gestion des déchets de soins, désinfection.",
            "icon": "Sparkles",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f4-1",
                    "titre": "Précautions standards",
                    "contenu": "Les précautions standards s'appliquent pour tout patient, quel que soit son statut infectieux.\n\n**Principes:**\n- Tout sang et liquide biologique est potentiellement infectieux\n- La protection est systématique\n- L'hygiène des mains est primordiale\n\n**Application:**\n- Port de gants pour tout contact avec du sang\n- Port de masque si risque de projection\n- Lavage des mains avant et après chaque intervention"
                },
                {
                    "id": "f4-2",
                    "titre": "Hygiène des mains",
                    "contenu": "**Lavage simple (savon doux):**\nDurée: 30 secondes minimum\n1. Mouiller les mains\n2. Appliquer le savon\n3. Frotter paumes, dos, entre les doigts, ongles\n4. Rincer abondamment\n5. Sécher avec essuie-mains à usage unique\n\n**Friction hydro-alcoolique (SHA):**\nDurée: 30 secondes minimum\n- Sur mains visiblement propres et sèches\n- Couvrir toute la surface des mains\n- Frotter jusqu'à séchage complet\n\n**Quand se laver les mains:**\n- Avant et après chaque intervention\n- Après retrait des gants\n- Après contact avec des surfaces souillées"
                },
                {
                    "id": "f4-3",
                    "titre": "Gestion des DASRI",
                    "contenu": "**DASRI**: Déchets d'Activités de Soins à Risques Infectieux\n\n**Types de déchets:**\n- Matériels piquants/coupants (aiguilles, lames)\n- Matériels souillés par du sang\n- Gants et compresses usagés\n\n**Conteneurs:**\n- Jaune: DASRI mous (compresses, gants)\n- Jaune avec couvercle: DASRI piquants/coupants\n\n**Règles:**\n- Ne jamais recapuchonner une aiguille\n- Jeter immédiatement après usage\n- Ne pas dépasser le niveau de remplissage\n- Fermer définitivement avant élimination"
                }
            ]
        },
        {
            "id": "ch5",
            "numero": 5,
            "titre": "Urgences vitales",
            "description": "Arrêt cardiaque, RCP, défibrillation, hémorragies, obstruction des voies aériennes, perte de connaissance.",
            "icon": "Heart",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f5-1",
                    "titre": "Arrêt cardiaque et RCP",
                    "contenu": "**Reconnaissance de l'arrêt cardiaque:**\n- Victime inconsciente\n- Absence de respiration normale (gasps possibles)\n\n**Conduite à tenir:**\n1. Alerter ou faire alerter (15, 18 ou 112)\n2. Demander un DAE\n3. Commencer la RCP immédiatement\n\n**RCP Adulte:**\n- 30 compressions / 2 insufflations\n- Fréquence: 100-120 compressions/min\n- Profondeur: 5-6 cm\n- Relâchement complet entre les compressions\n\n**RCP Enfant/Nourrisson:**\n- 5 insufflations initiales\n- Puis 15 compressions / 2 insufflations\n- Compressions: 1/3 du thorax"
                },
                {
                    "id": "f5-2",
                    "titre": "Défibrillation (DAE)",
                    "contenu": "**Le DAE (Défibrillateur Automatisé Externe):**\n- Analyse le rythme cardiaque\n- Délivre un choc si nécessaire\n- Guide l'utilisateur par messages vocaux\n\n**Utilisation:**\n1. Allumer le DAE\n2. Dénuder le thorax de la victime\n3. Coller les électrodes selon le schéma\n4. S'écarter pendant l'analyse\n5. Délivrer le choc si recommandé\n6. Reprendre immédiatement la RCP\n\n**Position des électrodes:**\n- Adulte: sous clavicule droite + sous aisselle gauche\n- Enfant < 8 ans: une sur le thorax, une dans le dos\n\n**Cas particuliers:**\n- Thorax mouillé: sécher avant de coller\n- Patch médicamenteux: retirer et nettoyer\n- Pacemaker: électrode à 8 cm minimum"
                },
                {
                    "id": "f5-3",
                    "titre": "Hémorragies externes",
                    "contenu": "**Définition:**\nSaignement abondant et visible suite à une plaie.\n\n**Conduite à tenir:**\n1. **Compression directe:**\n   - Appuyer fortement avec la main protégée\n   - Maintenir jusqu'à l'arrivée des secours\n\n2. **Pansement compressif:**\n   - Si la compression manuelle doit être relâchée\n   - Coussin hémostatique + bande\n\n3. **Garrot:**\n   - En dernier recours\n   - Membre inaccessible ou compression impossible\n   - Noter l'heure de pose\n   - Ne jamais desserrer\n\n**Positions d'attente:**\n- Allonger la victime\n- Surélever les jambes si possible\n- Couvrir pour éviter l'hypothermie"
                },
                {
                    "id": "f5-4",
                    "titre": "Obstruction des voies aériennes",
                    "contenu": "**Obstruction partielle:**\n- La victime tousse, peut parler\n- Encourager à tousser\n- Ne pas intervenir tant qu'elle tousse efficacement\n\n**Obstruction totale:**\n- La victime ne peut plus parler, tousser, respirer\n- Porte les mains à sa gorge\n\n**Conduite à tenir - Adulte/Enfant:**\n1. **5 claques dans le dos:**\n   - Pencher la victime en avant\n   - Frapper entre les omoplates\n\n2. **5 compressions abdominales (Heimlich):**\n   - Se placer derrière la victime\n   - Poing fermé au-dessus du nombril\n   - Compressions vers soi et vers le haut\n\n3. Alterner jusqu'à désobstruction ou perte de conscience\n\n**Nourrisson:**\n- 5 claques dans le dos (tête en bas)\n- 5 compressions thoraciques (2 doigts sur le sternum)"
                },
                {
                    "id": "f5-5",
                    "titre": "Perte de connaissance",
                    "contenu": "**Définition:**\nLa victime ne répond pas mais respire.\n\n**Risques:**\n- Obstruction des voies aériennes par la langue\n- Inhalation de vomissements\n\n**Conduite à tenir:**\n1. Vérifier la conscience (stimulation verbale et douloureuse)\n2. Libérer les voies aériennes (bascule de la tête)\n3. Vérifier la respiration (10 secondes)\n4. Mettre en Position Latérale de Sécurité (PLS)\n5. Alerter les secours\n6. Surveiller la respiration\n\n**PLS - Points clés:**\n- Maintenir les voies aériennes libres\n- Position stable\n- Permettre l'écoulement des liquides\n- Surveiller en permanence"
                }
            ]
        },
        {
            "id": "ch6",
            "numero": 6,
            "titre": "Malaises et affections spécifiques",
            "description": "AVC, crise convulsive, asthme, douleur thoracique, hypoglycémie, réaction allergique.",
            "icon": "Activity",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f6-1",
                    "titre": "Accident Vasculaire Cérébral (AVC)",
                    "contenu": "**Définition:**\nArrêt brutal de la circulation sanguine dans une partie du cerveau.\n\n**Signes (Score FAST):**\n- **F**ace: asymétrie du visage, bouche de travers\n- **A**rm: faiblesse ou paralysie d'un bras\n- **S**peech: difficultés à parler, propos incohérents\n- **T**ime: noter l'heure de début des symptômes\n\n**Autres signes:**\n- Maux de tête violents et soudains\n- Troubles de la vision\n- Perte d'équilibre\n- Confusion\n\n**Conduite à tenir:**\n1. Alerter immédiatement le 15\n2. Allonger la victime (tête légèrement surélevée)\n3. Ne rien donner à boire ou à manger\n4. Noter l'heure des premiers symptômes\n5. Surveiller en permanence"
                },
                {
                    "id": "f6-2",
                    "titre": "Crise convulsive",
                    "contenu": "**Définition:**\nContractions musculaires involontaires dues à une activité électrique anormale du cerveau.\n\n**Phases de la crise:**\n1. Phase tonique: raidissement généralisé\n2. Phase clonique: secousses musculaires\n3. Phase de récupération: confusion, fatigue\n\n**Conduite à tenir pendant la crise:**\n- Ne pas maintenir la victime\n- Écarter les objets dangereux\n- Protéger la tête\n- Ne rien mettre dans la bouche\n\n**Après la crise:**\n- Mettre en PLS si inconsciente\n- Rassurer au réveil\n- Alerter si: première crise, crise > 5 min, crises répétées, traumatisme associé"
                },
                {
                    "id": "f6-3",
                    "titre": "Crise d'asthme",
                    "contenu": "**Définition:**\nDifficultés respiratoires dues à un rétrécissement des bronches.\n\n**Signes:**\n- Sifflements à l'expiration\n- Difficultés à parler (phrases courtes)\n- Position assise penchée en avant\n- Angoisse\n\n**Signes de gravité:**\n- Cyanose (lèvres, ongles bleutés)\n- Sueurs\n- Impossibilité de parler\n- Épuisement\n\n**Conduite à tenir:**\n1. Mettre en position assise ou demi-assise\n2. Rassurer, calmer\n3. Aider à la prise du traitement (bronchodilatateur)\n4. Alerter le 15 si crise sévère ou traitement inefficace\n5. Administrer de l'oxygène si disponible"
                },
                {
                    "id": "f6-4",
                    "titre": "Réaction allergique grave (Anaphylaxie)",
                    "contenu": "**Définition:**\nRéaction allergique sévère pouvant mettre en jeu le pronostic vital.\n\n**Allergènes fréquents:**\n- Aliments (arachides, fruits de mer, œufs)\n- Médicaments\n- Piqûres d'insectes\n- Latex\n\n**Signes:**\n- Urticaire, œdème du visage\n- Difficultés respiratoires\n- Gonflement de la gorge\n- Chute de tension, malaise\n\n**Conduite à tenir:**\n1. Alerter immédiatement le 15\n2. Position adaptée:\n   - Détresse respiratoire: position assise\n   - Malaise: position allongée, jambes surélevées\n3. Aider à l'injection d'adrénaline si auto-injecteur disponible\n4. Être prêt à faire la RCP"
                }
            ]
        },
        {
            "id": "ch7",
            "numero": 7,
            "titre": "Atteintes circonstancielles",
            "description": "Accidents électriques, noyade, intoxications, brûlures, plaies, hypothermie, hyperthermie.",
            "icon": "AlertTriangle",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f7-1",
                    "titre": "Accident électrique",
                    "contenu": "**Types d'accidents:**\n- Électrisation: passage du courant dans le corps\n- Électrocution: électrisation mortelle\n\n**Dangers:**\n- Arrêt cardiaque\n- Brûlures internes et externes\n- Tétanisation musculaire\n\n**Conduite à tenir:**\n1. **Couper le courant** avant tout contact\n2. Si impossible: éloigner la victime avec un objet isolant (bois sec)\n3. Alerter les secours\n4. Rechercher les brûlures (entrée et sortie du courant)\n5. Surveiller les fonctions vitales\n6. Être prêt à réanimer\n\n**Attention:**\nLes lésions internes peuvent être graves même si les brûlures visibles sont minimes."
                },
                {
                    "id": "f7-2",
                    "titre": "Noyade",
                    "contenu": "**Définition:**\nDétresse respiratoire par inhalation d'eau.\n\n**Stades:**\n1. Aquastress: angoisse sans inhalation\n2. Petit hypoxique: inhalation modérée\n3. Grand hypoxique: inhalation importante, coma\n4. Anoxique: arrêt cardiaque\n\n**Conduite à tenir:**\n1. Sortir la victime de l'eau (sans se mettre en danger)\n2. Alerter les secours\n3. Si consciente: déshabiller, sécher, réchauffer\n4. Si inconsciente qui respire: PLS et surveillance\n5. Si arrêt cardiaque: RCP (commencer par 5 insufflations)\n\n**Particularités:**\n- Hypothermie fréquente associée\n- Ne pas faire de manœuvres pour vider l'eau"
                },
                {
                    "id": "f7-3",
                    "titre": "Brûlures",
                    "contenu": "**Types de brûlures:**\n- Thermiques (chaleur, froid)\n- Chimiques (acides, bases)\n- Électriques\n- Radiologiques\n\n**Gravité selon:**\n- Étendue (règle des 9 de Wallace)\n- Profondeur (1er, 2e, 3e degré)\n- Localisation (visage, mains, périnée)\n- Âge et état de santé\n\n**Conduite à tenir - Brûlure thermique:**\n1. Supprimer la cause\n2. Refroidir à l'eau tempérée (15-20°C) pendant 10-15 min\n3. Retirer les vêtements non adhérents\n4. Protéger par un pansement stérile\n5. Alerter si brûlure étendue ou grave\n\n**Brûlure chimique:**\n- Rinçage abondant et prolongé (20-30 min)\n- Retirer les vêtements souillés pendant le rinçage"
                },
                {
                    "id": "f7-4",
                    "titre": "Hypothermie",
                    "contenu": "**Définition:**\nTemperature centrale < 35°C\n\n**Stades:**\n- Légère (35-32°C): frissons, confusion légère\n- Modérée (32-28°C): arrêt des frissons, somnolence\n- Sévère (< 28°C): coma, risque d'arrêt cardiaque\n\n**Conduite à tenir:**\n1. Soustraire du froid\n2. Retirer les vêtements mouillés\n3. Réchauffement passif: couvertures, couverture de survie (côté doré vers l'extérieur)\n4. Pas de réchauffement actif rapide (risque cardiaque)\n5. Position allongée\n6. Alerter les secours\n\n**Attention:**\n- Manipuler avec précaution (risque de fibrillation)\n- Ne pas donner de boissons alcoolisées"
                }
            ]
        },
        {
            "id": "ch8",
            "numero": 8,
            "titre": "Traumatismes",
            "description": "Traumatismes crâniens, du rachis, du thorax, de l'abdomen, des membres. Immobilisation.",
            "icon": "Bone",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f8-1",
                    "titre": "Traumatisme crânien",
                    "contenu": "**Mécanismes:**\n- Choc direct sur la tête\n- Décélération brutale\n\n**Signes de gravité:**\n- Perte de connaissance (même brève)\n- Confusion, désorientation\n- Maux de tête intenses\n- Vomissements\n- Troubles de la vision\n- Écoulement par le nez ou les oreilles\n\n**Conduite à tenir:**\n1. Maintenir l'axe tête-cou-tronc\n2. Ne pas mobiliser sauf danger vital\n3. Surveiller la conscience (EVDA)\n4. Alerter les secours\n5. Si inconscient qui respire: PLS à 2 équipiers minimum\n\n**Toujours suspecter une lésion du rachis associée**"
                },
                {
                    "id": "f8-2",
                    "titre": "Traumatisme du rachis",
                    "contenu": "**Mécanismes à risque:**\n- Accident de la route\n- Chute de hauteur\n- Plongeon en eau peu profonde\n- Coup violent sur la tête ou le dos\n\n**Signes:**\n- Douleur à la colonne vertébrale\n- Fourmillements dans les membres\n- Perte de sensibilité\n- Impossibilité de bouger les membres\n\n**Conduite à tenir:**\n1. Ne pas mobiliser la victime\n2. Maintenir la tête en position neutre\n3. Demander à la victime de ne pas bouger\n4. Alerter les secours spécialisés\n5. Protéger du froid\n\n**Immobilisation:**\n- Collier cervical\n- Plan dur ou matelas à dépression\n- Respect de l'axe tête-cou-tronc"
                },
                {
                    "id": "f8-3",
                    "titre": "Traumatisme des membres",
                    "contenu": "**Types de lésions:**\n- Fracture: rupture de l'os\n- Luxation: déboîtement d'une articulation\n- Entorse: atteinte des ligaments\n\n**Signes:**\n- Douleur vive\n- Déformation visible\n- Gonflement\n- Impotence fonctionnelle\n- Parfois plaie (fracture ouverte)\n\n**Conduite à tenir:**\n1. Ne pas mobiliser le membre\n2. Immobiliser dans la position trouvée\n3. Vérifier la sensibilité et le pouls en aval\n4. Recouvrir une plaie éventuelle\n5. Appliquer du froid si possible\n6. Alerter les secours\n\n**Immobilisation:**\n- Attelle modelable ou à dépression\n- Écharpe pour le membre supérieur\n- Pas de réalignement sauf si absence de pouls"
                }
            ]
        },
        {
            "id": "ch9",
            "numero": 9,
            "titre": "Souffrance psychique",
            "description": "Situations de crise, comportements inhabituels, agressivité, gestion du stress.",
            "icon": "Brain",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f9-1",
                    "titre": "Situations de crise",
                    "contenu": "**Définition:**\nÉtat de décompensation psychologique aigu.\n\n**Causes:**\n- Événement traumatisant\n- Annonce d'un décès\n- Catastrophe\n- Stress intense\n\n**Manifestations:**\n- Agitation ou prostration\n- Pleurs, cris\n- Confusion\n- Hyperventilation\n\n**Conduite à tenir:**\n1. Assurer la sécurité\n2. S'approcher calmement\n3. Se présenter\n4. Écouter sans juger\n5. Parler lentement et clairement\n6. Rester présent\n7. Éviter les foules autour"
                },
                {
                    "id": "f9-2",
                    "titre": "Comportement agressif",
                    "contenu": "**Causes possibles:**\n- Stress extrême\n- Intoxication (alcool, drogues)\n- Pathologie psychiatrique\n- Hypoglycémie\n- Traumatisme crânien\n\n**Signes précurseurs:**\n- Agitation croissante\n- Propos menaçants\n- Posture menaçante\n\n**Conduite à tenir:**\n1. **Ne jamais se mettre en danger**\n2. Garder ses distances\n3. Rester calme, parler doucement\n4. Ne pas défier du regard\n5. Proposer une issue non violente\n6. Alerter les forces de l'ordre si nécessaire\n7. Se replier si la situation dégénère\n\n**Attention:** La sécurité du secouriste prime"
                },
                {
                    "id": "f9-3",
                    "titre": "Risque suicidaire",
                    "contenu": "**Signes d'alerte:**\n- Propos sur la mort, le suicide\n- Don d'objets personnels\n- Isolement soudain\n- Changement brutal de comportement\n\n**Conduite à tenir:**\n1. Ne pas laisser seul\n2. Écouter sans juger\n3. Poser des questions directes (sans suggestion de méthode)\n4. Prendre au sérieux toute menace\n5. Alerter le 15 ou les secours psychiatriques\n6. Éloigner les moyens de passage à l'acte\n\n**À éviter:**\n- Minimiser la souffrance\n- Faire des reproches\n- Promettre le secret\n- Défier ('tu n'oseras pas')"
                }
            ]
        },
        {
            "id": "ch10",
            "numero": 10,
            "titre": "Relevage et brancardage",
            "description": "Techniques de relevage, brancardage, installation dans un véhicule de transport.",
            "icon": "Truck",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f10-1",
                    "titre": "Principes du relevage",
                    "contenu": "**Objectif:**\nTransférer une victime du sol vers un brancard en toute sécurité.\n\n**Principes:**\n- Maintenir l'axe tête-cou-tronc\n- Minimiser les mouvements\n- Coordonner les actions\n- Protéger le dos des secouristes\n\n**Techniques selon la situation:**\n- Pont simple ou amélioré\n- Cuillère (brancard cuillère)\n- Pont néerlandais\n- Relevage avec plan dur\n\n**Commandements:**\n- Un secouriste dirige la manœuvre\n- Ordres clairs et précis\n- 'Êtes-vous prêts?' - 'Attention pour lever... Levez!'"
                },
                {
                    "id": "f10-2",
                    "titre": "Techniques de brancardage",
                    "contenu": "**Règles générales:**\n- Progression régulière\n- Brancard horizontal\n- Tête de la victime dans le sens de la marche\n- Communication permanente\n\n**Brancardage en terrain plat:**\n- 4 secouristes aux 4 coins\n- Pas alternés\n\n**Brancardage en escalier:**\n- Descente: pieds de la victime en premier\n- Montée: tête de la victime en premier\n- Maintenir le brancard horizontal\n\n**Brancardage en pente:**\n- Descente: pieds en premier\n- Montée: tête en premier\n- Maintenir horizontal"
                },
                {
                    "id": "f10-3",
                    "titre": "Matériel de portage",
                    "contenu": "**Brancard principal:**\n- Support rigide avec sangles\n- Pieds ou roues\n- Dispositif de fixation\n\n**Brancard cuillère:**\n- S'ouvre en deux parties\n- Glisse sous la victime\n- Utilisé pour le relevage\n\n**Plan dur:**\n- Surface rigide\n- Pour traumatismes du rachis\n- Avec immobilisateur de tête\n\n**Matelas à dépression:**\n- Moulage du corps\n- Immobilisation complète\n- Confort de la victime\n\n**Chaise de transport:**\n- Pour victimes assises\n- Escaliers étroits"
                }
            ]
        },
        {
            "id": "ch11",
            "numero": 11,
            "titre": "Situations particulières",
            "description": "Nombreuses victimes, situations d'exception, accouchement inopiné.",
            "icon": "Users",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f11-1",
                    "titre": "Nombreuses victimes",
                    "contenu": "**Définition:**\nSituation où le nombre de victimes dépasse les moyens immédiatement disponibles.\n\n**Principes:**\n- Alerte précoce et précise\n- Triage des victimes\n- Priorisation des soins\n- Organisation des secours\n\n**Catégories de triage:**\n- **Rouge (UA)**: Urgence Absolue - pronostic vital engagé\n- **Jaune (UR)**: Urgence Relative - blessé grave mais stable\n- **Vert (EU)**: Éclopé/Impliqué - blessé léger\n- **Noir**: Décédé\n\n**Rôle du premier secouriste:**\n1. Évaluer rapidement la situation\n2. Alerter avec précision (nombre de victimes, lieu exact)\n3. Commencer le triage\n4. Prioriser les gestes qui sauvent"
                },
                {
                    "id": "f11-2",
                    "titre": "Accouchement inopiné",
                    "contenu": "**Signes de l'accouchement imminent:**\n- Contractions rapprochées (< 5 min)\n- Envie de pousser\n- Perte des eaux\n- Visualisation de la tête\n\n**Conduite à tenir:**\n1. Alerter le 15\n2. Préparer un espace propre et chaud\n3. Installer la mère en position gynécologique\n4. Laisser l'accouchement se faire naturellement\n5. Accompagner la sortie de la tête\n6. Vérifier l'absence de circulaire du cordon\n7. Soutenir le corps lors de l'expulsion\n8. Sécher et couvrir le nouveau-né\n9. Le poser sur le ventre de la mère\n10. Attendre les secours pour le cordon\n\n**Nouveau-né:**\n- Sécher, stimuler, réchauffer\n- S'assurer qu'il respire et crie"
                }
            ]
        },
        {
            "id": "ch12",
            "numero": 12,
            "titre": "Divers",
            "description": "Utilisation de l'oxygène, gestes complémentaires, abréviations.",
            "icon": "BookOpen",
            "formation_type": "PSE",
            "fiches": [
                {
                    "id": "f12-1",
                    "titre": "Administration d'oxygène",
                    "contenu": "**Indications:**\n- Détresse respiratoire\n- Détresse circulatoire\n- Intoxication au CO\n- Arrêt cardiaque\n\n**Matériel:**\n- Bouteille d'oxygène (blanche)\n- Manodétendeur-débitmètre\n- Dispositifs d'administration\n\n**Débits recommandés:**\n- Masque haute concentration: 12-15 L/min (SpO2 < 94%)\n- Masque simple: 6-10 L/min\n- Lunettes: 1-6 L/min\n\n**Précautions:**\n- Pas de flamme ni d'étincelle\n- Vérifier la pression avant utilisation\n- Adapter le débit à la saturation"
                },
                {
                    "id": "f12-2",
                    "titre": "Abréviations courantes",
                    "contenu": "**Sigles médicaux:**\n- AVC: Accident Vasculaire Cérébral\n- ACR: Arrêt Cardio-Respiratoire\n- DAE: Défibrillateur Automatisé Externe\n- RCP: Réanimation Cardio-Pulmonaire\n- PLS: Position Latérale de Sécurité\n- SpO2: Saturation en Oxygène\n- FC: Fréquence Cardiaque\n- FR: Fréquence Respiratoire\n- PA: Pression Artérielle\n- EVDA: Éveil, Voix, Douleur, Aucune réaction\n\n**Sigles d'organisation:**\n- SAMU: Service d'Aide Médicale Urgente\n- SMUR: Service Mobile d'Urgence et de Réanimation\n- PSE: Premiers Secours en Équipe\n- EPI: Équipement de Protection Individuelle\n- DASRI: Déchets d'Activités de Soins à Risques Infectieux"
                },
                {
                    "id": "f12-3",
                    "titre": "Numéros d'urgence",
                    "contenu": "**En France:**\n- **15**: SAMU (urgences médicales)\n- **18**: Pompiers (incendie, accidents)\n- **17**: Police/Gendarmerie\n- **112**: Numéro d'urgence européen\n- **114**: Urgences par SMS (sourds et malentendants)\n- **115**: SAMU social\n- **119**: Enfance en danger\n\n**Informations à transmettre:**\n1. Qui appelle (nom, fonction)\n2. Lieu précis (adresse, repères)\n3. Nature du problème\n4. Nombre de victimes\n5. État des victimes\n6. Gestes déjà effectués\n7. Ne jamais raccrocher en premier"
                }
            ]
        }
    ]
    
    for chapter in chapters:
        await db.chapters.insert_one(chapter)
    
    # Seed quizzes for PSE chapters
    quizzes = [
        {
            "id": "quiz-ch1",
            "chapter_id": "ch1",
            "titre": "Quiz - Attitude et comportement",
            "video_url": None,
            "questions": [
                {
                    "id": "q1-1",
                    "question": "Quelles sont les qualités essentielles d'un secouriste?",
                    "type": "qcm",
                    "options": ["Rapidité et force physique", "Organisation, rigueur, calme et humilité", "Autorité et commandement", "Impassibilité et froideur"],
                    "correct_answer": 1,
                    "explication": "Un secouriste doit être organisé, rigoureux, calme et humble pour intervenir efficacement."
                },
                {
                    "id": "q1-2",
                    "question": "Le secouriste bénéficie d'une protection juridique lorsqu'il porte assistance.",
                    "type": "vrai_faux",
                    "options": ["Vrai", "Faux"],
                    "correct_answer": 0,
                    "explication": "L'article 122-7 du Code pénal protège les personnes qui accomplissent un acte commandé par la nécessité de sauvegarder une vie."
                },
                {
                    "id": "q1-3",
                    "question": "Après une intervention difficile, quels signes doivent alerter le secouriste sur son état psychologique?",
                    "type": "qcm",
                    "options": ["Fatigue normale après l'effort", "Troubles du sommeil persistants et flashbacks récurrents", "Envie de raconter l'intervention", "Satisfaction du travail accompli"],
                    "correct_answer": 1,
                    "explication": "Les troubles du sommeil persistants, l'irritabilité et les flashbacks sont des signes d'alerte nécessitant une prise en charge."
                },
                {
                    "id": "q1-4",
                    "question": "Le secouriste peut mentir à la victime pour la rassurer.",
                    "type": "vrai_faux",
                    "options": ["Vrai", "Faux"],
                    "correct_answer": 1,
                    "explication": "Le secouriste doit rassurer sans mentir. La confiance est essentielle dans la relation avec la victime."
                },
                {
                    "id": "q1-5",
                    "question": "Quelle est la première chose à faire en arrivant sur les lieux d'un accident?",
                    "type": "qcm",
                    "options": ["Se précipiter vers la victime", "Protéger et sécuriser la zone", "Appeler les secours", "Prendre des photos"],
                    "correct_answer": 1,
                    "explication": "La protection est toujours la première étape pour éviter le sur-accident."
                }
            ]
        },
        {
            "id": "quiz-ch2",
            "chapter_id": "ch2",
            "titre": "Quiz - Bilans",
            "video_url": None,
            "questions": [
                {
                    "id": "q2-1",
                    "question": "Quelle est la fréquence respiratoire normale d'un adulte?",
                    "type": "qcm",
                    "options": ["5-10 cycles/min", "12-20 cycles/min", "30-40 cycles/min", "50-60 cycles/min"],
                    "correct_answer": 1,
                    "explication": "La fréquence respiratoire normale d'un adulte est de 12 à 20 cycles par minute."
                },
                {
                    "id": "q2-2",
                    "question": "Une saturation en oxygène (SpO2) de 92% est normale.",
                    "type": "vrai_faux",
                    "options": ["Vrai", "Faux"],
                    "correct_answer": 1,
                    "explication": "Une SpO2 normale est entre 95 et 100%. En dessous de 94%, elle est considérée comme insuffisante."
                },
                {
                    "id": "q2-3",
                    "question": "Que signifie le 'D' dans le score EVDA?",
                    "type": "qcm",
                    "options": ["Dialogue", "Douleur", "Détresse", "Danger"],
                    "correct_answer": 1,
                    "explication": "EVDA signifie: Éveillé, réagit à la Voix, réagit à la Douleur, Aucune réaction."
                },
                {
                    "id": "q2-4",
                    "question": "Le score de Glasgow est noté sur 15 points.",
                    "type": "vrai_faux",
                    "options": ["Vrai", "Faux"],
                    "correct_answer": 0,
                    "explication": "Le score de Glasgow évalue 3 paramètres (yeux, verbal, moteur) pour un total de 15 points."
                },
                {
                    "id": "q2-5",
                    "question": "Que recherche-t-on lors du 'deuxième regard'?",
                    "type": "qcm",
                    "options": ["Les dangers environnants", "Les menaces vitales immédiates", "Les antécédents médicaux", "L'identité de la victime"],
                    "correct_answer": 1,
                    "explication": "Le deuxième regard identifie les menaces vitales: hémorragie, étouffement, conscience, respiration."
                }
            ]
        },
        {
            "id": "quiz-ch5",
            "chapter_id": "ch5",
            "titre": "Quiz - Urgences vitales",
            "video_url": None,
            "questions": [
                {
                    "id": "q5-1",
                    "question": "Quelle est la fréquence recommandée pour les compressions thoraciques lors de la RCP?",
                    "type": "qcm",
                    "options": ["50-80 compressions/min", "100-120 compressions/min", "150-180 compressions/min", "200 compressions/min"],
                    "correct_answer": 1,
                    "explication": "La fréquence recommandée est de 100 à 120 compressions par minute."
                },
                {
                    "id": "q5-2",
                    "question": "Lors d'un arrêt cardiaque chez l'adulte, on commence par 5 insufflations.",
                    "type": "vrai_faux",
                    "options": ["Vrai", "Faux"],
                    "correct_answer": 1,
                    "explication": "Chez l'adulte, on commence directement par les compressions thoraciques. Les 5 insufflations initiales sont réservées aux enfants, nourrissons et noyés."
                },
                {
                    "id": "q5-3",
                    "question": "Quel est le rapport compressions/insufflations pour la RCP adulte?",
                    "type": "qcm",
                    "options": ["15/2", "30/2", "20/5", "10/1"],
                    "correct_answer": 1,
                    "explication": "Le rapport est de 30 compressions pour 2 insufflations chez l'adulte."
                },
                {
                    "id": "q5-4",
                    "question": "Un garrot une fois posé peut être desserré pour vérifier si le saignement s'est arrêté.",
                    "type": "vrai_faux",
                    "options": ["Vrai", "Faux"],
                    "correct_answer": 1,
                    "explication": "Un garrot ne doit jamais être desserré une fois posé. Cela peut provoquer des complications graves."
                },
                {
                    "id": "q5-5",
                    "question": "Face à une obstruction totale des voies aériennes chez l'adulte, quelle est la première technique à utiliser?",
                    "type": "qcm",
                    "options": ["Compressions abdominales (Heimlich)", "5 claques dans le dos", "Ventilation bouche-à-bouche", "Position latérale de sécurité"],
                    "correct_answer": 1,
                    "explication": "On commence par 5 claques dans le dos, puis si inefficace, 5 compressions abdominales."
                }
            ]
        }
    ]
    
    for quiz in quizzes:
        await db.quizzes.insert_one(quiz)
    
    # Create placeholder chapters for PSC and BNSSA
    psc_chapter = {
        "id": "psc-1",
        "numero": 1,
        "titre": "Premiers Secours Citoyen - Introduction",
        "description": "Contenu à venir - Formation aux gestes de premiers secours pour le grand public.",
        "icon": "Heart",
        "formation_type": "PSC",
        "fiches": [
            {
                "id": "psc-1-1",
                "titre": "Introduction au PSC",
                "contenu": "Contenu en cours de création. Cette section présentera les bases des premiers secours accessibles à tous les citoyens."
            }
        ]
    }
    await db.chapters.insert_one(psc_chapter)
    
    bnssa_chapter = {
        "id": "bnssa-1",
        "numero": 1,
        "titre": "BNSSA - Introduction",
        "description": "Contenu à venir - Formation au sauvetage aquatique.",
        "icon": "Waves",
        "formation_type": "BNSSA",
        "fiches": [
            {
                "id": "bnssa-1-1",
                "titre": "Introduction au BNSSA",
                "contenu": "Contenu en cours de création. Cette section présentera la formation au Brevet National de Sécurité et Sauvetage Aquatique."
            }
        ]
    }
    await db.chapters.insert_one(bnssa_chapter)
    
    # Create 8 PSC chapters
    psc_chapters = [
        {
            "id": "psc1-ch1",
            "numero": 1,
            "titre": "Informations générales et Protection",
            "description": "Le citoyen de sécurité civile, alerte et protection des populations, principes de protection.",
            "icon": "Shield",
            "formation_type": "PSC",
            "fiches": [{"id": "psc1-f1-1", "titre": "Le citoyen de Sécurité Civile", "contenu": "Protection juridique et messages clés sur la prévention des accidents."}]
        },
        {
            "id": "psc1-ch2",
            "numero": 2,
            "titre": "Obstruction des voies aériennes",
            "description": "Reconnaître une obstruction totale ou partielle, manœuvres de désobstruction.",
            "icon": "Wind",
            "formation_type": "PSC",
            "fiches": [{"id": "psc1-f2-1", "titre": "Obstruction totale", "contenu": "Claques dans le dos et compressions abdominales (Heimlich)."}]
        },
        {
            "id": "psc1-ch3",
            "numero": 3,
            "titre": "Hémorragies externes",
            "description": "Reconnaître une hémorragie, compression directe, pansement compressif.",
            "icon": "Droplet",
            "formation_type": "PSC",
            "fiches": [{"id": "psc1-f3-1", "titre": "Compression directe", "contenu": "Appuyer fortement sur la plaie avec un linge propre."}]
        },
        {
            "id": "psc1-ch4",
            "numero": 4,
            "titre": "Perte de connaissance",
            "description": "Vérifier la conscience, libérer les voies aériennes, PLS.",
            "icon": "UserX",
            "formation_type": "PSC",
            "fiches": [{"id": "psc1-f4-1", "titre": "Position Latérale de Sécurité", "contenu": "Mettre la victime sur le côté pour éviter l'étouffement."}]
        },
        {
            "id": "psc1-ch5",
            "numero": 5,
            "titre": "Arrêt cardiaque",
            "description": "Massage cardiaque, utilisation du DAE, insufflations.",
            "icon": "Heart",
            "formation_type": "PSC",
            "fiches": [{"id": "psc1-f5-1", "titre": "Réanimation cardio-pulmonaire", "contenu": "30 compressions thoraciques puis 2 insufflations, rythme 100-120/min."}]
        },
        {
            "id": "psc1-ch6",
            "numero": 6,
            "titre": "Malaises",
            "description": "Reconnaître un malaise, mettre au repos, alerter si nécessaire.",
            "icon": "AlertCircle",
            "formation_type": "PSC",
            "fiches": [{"id": "psc1-f6-1", "titre": "Conduite à tenir", "contenu": "Mettre la victime au repos, desserrer les vêtements, alerter le 15."}]
        },
        {
            "id": "psc1-ch7",
            "numero": 7,
            "titre": "Plaies et Brûlures",
            "description": "Plaies simples et graves, brûlures thermiques, chimiques, électriques.",
            "icon": "Flame",
            "formation_type": "PSC",
            "fiches": [{"id": "psc1-f7-1", "titre": "Plaies graves", "contenu": "Ne pas retirer le corps étranger, protéger avec un pansement stérile."}]
        },
        {
            "id": "psc1-ch8",
            "numero": 8,
            "titre": "Traumatismes",
            "description": "Traumatismes des os et articulations, immobilisation, surveillance.",
            "icon": "Bone",
            "formation_type": "PSC",
            "fiches": [{"id": "psc1-f8-1", "titre": "Immobilisation", "contenu": "Immobiliser dans la position trouvée, ne pas mobiliser en cas de douleur."}]
        }
    ]
    
    for psc_chapter in psc_chapters:
        await db.chapters.insert_one(psc_chapter)
    
    # Create quiz for ALL chapters (PSE + PSC)
    all_chapters = await db.chapters.find({}, {"_id": 0}).to_list(100)
    for chapter in all_chapters:
        # Create quiz with 2-5 questions depending on formation type
        num_questions = 5 if chapter["formation_type"] == "PSE" else 2
        questions = []
        
        for i in range(num_questions):
            if i % 2 == 0:
                questions.append({
                    "id": f"q{i+1}-{chapter['id']}",
                    "question": f"Quelle est l'action prioritaire pour {chapter['titre']} ?",
                    "type": "qcm",
                    "options": ["Option A", "Option B - Correcte", "Option C", "Option D"],
                    "correct_answer": 1,
                    "explication": f"L'action prioritaire pour {chapter['titre']} est décrite dans le référentiel 2024."
                })
            else:
                questions.append({
                    "id": f"q{i+1}-{chapter['id']}",
                    "question": f"Cette affirmation sur {chapter['titre']} est vraie",
                    "type": "vrai_faux",
                    "correct_answer": True,
                    "explication": f"Cette affirmation est conforme au référentiel {chapter['titre']}."
                })
        
        quiz = {
            "id": f"quiz-{chapter['id']}",
            "chapter_id": chapter["id"],
            "formation_type": chapter["formation_type"],
            "questions": questions
        }
        await db.quizzes.insert_one(quiz)
    
    users_count = await db.users.count_documents({})
    chapters_count = await db.chapters.count_documents({})
    quizzes_count = await db.quizzes.count_documents({})
    
    # Set seed flag to prevent re-seeding
    await db.system_flags.insert_one({
        "flag": "database_seeded",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "version": "1.0"
    })
    
    return {
        "message": "Base de données initialisée avec succès",
        "admin_email": "ledisque.tanguy73@hotmail.com",
        "admin_password": "NewAdmin123!",
        "formateur_email": "test@secours73.fr",
        "stagiaire_email": "stagiaire.test@secours73.fr",
        "test_password": "test123",
        "users_created": users_count,
        "chapters_created": chapters_count,
        "quizzes_created": quizzes_count
    }

# ============== SITE SETTINGS ==============

@api_router.get("/settings")
async def get_site_settings():
    """Get public site settings (HelloAsso link, images)"""
    settings = await db.site_settings.find_one({"type": "general"}, {"_id": 0})
    if not settings:
        settings = {
            "type": "general",
            "helloasso_url": "",
            "helloasso_enabled": False
        }
    
    images = await db.site_images.find({}, {"_id": 0}).sort("order", 1).to_list(100)
    
    return {
        "helloasso_url": settings.get("helloasso_url", ""),
        "helloasso_enabled": settings.get("helloasso_enabled", False),
        "images": images
    }

@api_router.put("/admin/settings")
async def update_site_settings(
    settings: SiteSettingsUpdate,
    token: str = Query(...)
):
    """Update site settings (Admin only)"""
    user = await get_current_user(token)
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    update_data = {k: v for k, v in settings.model_dump().items() if v is not None}
    if update_data:
        await db.site_settings.update_one(
            {"type": "general"},
            {"$set": update_data},
            upsert=True
        )
    
    return {"message": "Paramètres mis à jour"}

@api_router.get("/admin/images")
async def get_site_images(token: str = Query(...)):
    """Get all site images (Admin only)"""
    user = await get_current_user(token)
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    images = await db.site_images.find({}, {"_id": 0}).sort("order", 1).to_list(100)
    return images

@api_router.post("/admin/images")
async def create_site_image(
    image: SiteImageCreate,
    token: str = Query(...)
):
    """Add a new site image (Admin only)"""
    user = await get_current_user(token)
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    image_doc = {
        "id": str(uuid.uuid4()),
        "name": image.name,
        "url": image.url,
        "alt_text": image.alt_text,
        "section": image.section,
        "order": image.order,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.site_images.insert_one(image_doc)
    image_doc.pop("_id", None)
    
    return {"message": "Image ajoutée", "image": image_doc}

@api_router.put("/admin/images/{image_id}")
async def update_site_image(
    image_id: str,
    image: SiteImageUpdate,
    token: str = Query(...)
):
    """Update a site image (Admin only)"""
    user = await get_current_user(token)
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    update_data = {k: v for k, v in image.model_dump().items() if v is not None}
    if update_data:
        result = await db.site_images.update_one(
            {"id": image_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Image non trouvée")
    
    return {"message": "Image mise à jour"}

@api_router.delete("/admin/images/{image_id}")
async def delete_site_image(
    image_id: str,
    token: str = Query(...)
):
    """Delete a site image (Admin only)"""
    user = await get_current_user(token)
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    
    result = await db.site_images.delete_one({"id": image_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Image non trouvée")
    
    return {"message": "Image supprimée"}


# ============== PASSWORD RESET ==============

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

@api_router.post("/auth/forgot-password")
async def forgot_password(request: PasswordResetRequest):
    """Demande de réinitialisation de mot de passe"""
    user = await db.users.find_one({"email": request.email})
    
    if not user:
        # Ne pas révéler si l'email existe ou non (sécurité)
        return {"message": "Si cet email existe, un lien de réinitialisation a été envoyé"}
    
    # Générer un token unique
    reset_token = secrets.token_urlsafe(32)
    
    # Sauvegarder le token avec expiration (1 heure)
    from datetime import datetime, timedelta
    expiration = datetime.now() + timedelta(hours=1)
    
    await db.users.update_one(
        {"email": request.email},
        {"$set": {
            "reset_token": reset_token,
            "reset_token_expiration": expiration.isoformat()
        }}
    )
    
    # Envoyer l'email
    reset_url = f"https://secours73.fr/reset-password?token={reset_token}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #dc2626;">Réinitialisation de mot de passe</h2>
        <p>Bonjour {user.get('prenom', '')} {user.get('nom', '')},</p>
        <p>Vous avez demandé à réinitialiser votre mot de passe sur la plateforme Secours 73.</p>
        <p>Cliquez sur le bouton ci-dessous pour créer un nouveau mot de passe :</p>
        <p style="text-align: center; margin: 30px 0;">
            <a href="{reset_url}" style="background-color: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Réinitialiser mon mot de passe
            </a>
        </p>
        <p style="color: #666; font-size: 14px;">
            Ce lien est valable pendant 1 heure.<br>
            Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.
        </p>
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        <p style="color: #999; font-size: 12px;">
            L'équipe pédagogique<br>
            Secours 73
        </p>
    </body>
    </html>
    """
    
    await send_email(request.email, "Réinitialisation de votre mot de passe - Secours 73", html_content)
    
    return {"message": "Si cet email existe, un lien de réinitialisation a été envoyé"}

@api_router.post("/auth/reset-password")
async def reset_password(request: PasswordResetConfirm):
    """Réinitialiser le mot de passe avec le token"""
    from datetime import datetime
    
    user = await db.users.find_one({"reset_token": request.token})
    
    if not user:
        raise HTTPException(status_code=400, detail="Token invalide ou expiré")
    
    # Vérifier l'expiration
    expiration = datetime.fromisoformat(user.get('reset_token_expiration', ''))
    if datetime.now() > expiration:
        raise HTTPException(status_code=400, detail="Token expiré")
    
    # Changer le mot de passe
    hashed_password = hash_password(request.new_password)
    
    await db.users.update_one(
        {"reset_token": request.token},
        {
            "$set": {"password": hashed_password},
            "$unset": {"reset_token": "", "reset_token_expiration": ""}
        }
    )
    
    return {"message": "Mot de passe réinitialisé avec succès"}


# ============== MESSAGERIE INTERNE ==============

class MessageCreate(BaseModel):
    destinataire_id: str
    sujet: str
    contenu: str

class MessageResponse(BaseModel):
    id: str
    expediteur_id: str
    expediteur_nom: str
    expediteur_prenom: str
    destinataire_id: str
    destinataire_nom: str
    destinataire_prenom: str
    sujet: str
    contenu: str
    lu: bool
    date_envoi: str

@api_router.post("/messages")
async def send_message(message: MessageCreate, token: str):
    """Envoyer un message interne"""
    user = await require_auth(token)
    
    # Vérifier que le destinataire existe
    destinataire = await db.users.find_one({"id": message.destinataire_id})
    if not destinataire:
        raise HTTPException(status_code=404, detail="Destinataire non trouvé")
    
    # Créer le message
    new_message = {
        "id": str(uuid.uuid4()),
        "expediteur_id": user['id'],
        "expediteur_nom": user['nom'],
        "expediteur_prenom": user['prenom'],
        "expediteur_role": user['role'],
        "destinataire_id": message.destinataire_id,
        "destinataire_nom": destinataire['nom'],
        "destinataire_prenom": destinataire['prenom'],
        "destinataire_role": destinataire['role'],
        "sujet": message.sujet,
        "contenu": message.contenu,
        "lu": False,
        "date_envoi": datetime.now().isoformat()
    }
    
    await db.messages.insert_one(new_message)
    
    return {"message": "Message envoyé", "id": new_message["id"]}

@api_router.get("/messages/received")
async def get_received_messages(token: str):
    """Récupérer les messages reçus"""
    user = await require_auth(token)
    
    messages = await db.messages.find(
        {"destinataire_id": user['id']},
        {"_id": 0}
    ).sort("date_envoi", -1).to_list(100)
    
    return messages

@api_router.get("/messages/sent")
async def get_sent_messages(token: str):
    """Récupérer les messages envoyés"""
    user = await require_auth(token)
    
    messages = await db.messages.find(
        {"expediteur_id": user['id']},
        {"_id": 0}
    ).sort("date_envoi", -1).to_list(100)
    
    return messages

@api_router.put("/messages/{message_id}/read")
async def mark_message_as_read(message_id: str, token: str):
    """Marquer un message comme lu"""
    user = await require_auth(token)
    
    result = await db.messages.update_one(
        {"id": message_id, "destinataire_id": user['id']},
        {"$set": {"lu": True}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    
    return {"message": "Message marqué comme lu"}

@api_router.get("/messages/unread-count")
async def get_unread_count(token: str):
    """Nombre de messages non lus"""
    user = await require_auth(token)
    
    count = await db.messages.count_documents({
        "destinataire_id": user['id'],
        "lu": False
    })
    
    return {"count": count}


# ============== EMAIL SENDING (Formateurs) ==============

@api_router.post("/admin/send-welcome-email")
async def send_welcome_email_to_stagiaire(stagiaire_email: str, token: str):
    """Admin/Formateur envoie l'email de bienvenue à un stagiaire"""
    user = await require_auth(token)
    
    if user['role'] not in ['formateur', 'admin']:
        raise HTTPException(status_code=403, detail="Accès réservé aux formateurs/admin")
    
    # Récupérer les infos du stagiaire
    stagiaire = await db.users.find_one({"email": stagiaire_email})
    if not stagiaire:
        raise HTTPException(status_code=404, detail="Stagiaire non trouvé")
    
    html_content = """
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #dc2626;">Bienvenue sur la plateforme de formation</h2>
        <p>Bonjour,</p>
        <p>Bienvenue sur la plateforme de formation ouverte à distance développée par <strong>Secours Alpes 73</strong>.</p>
        <p>Nous sommes ravis de vous accueillir pour cette première partie de votre formation.</p>
        <p>Cette plateforme a été conçue pour vous permettre d'apprendre à votre rythme et d'accéder facilement aux ressources pédagogiques mises à votre disposition.</p>
        <p>L'ensemble de l'équipe pédagogique vous souhaite une excellente formation et reste à votre disposition pour répondre à toutes vos questions ou vous accompagner si nécessaire.</p>
        <p style="margin-top: 30px;">Bonne formation et à très bientôt sur la plateforme.</p>
        <p style="margin-top: 30px;">Cordialement,</p>
        <p><strong>L'équipe pédagogique<br>Secours 73</strong></p>
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        <p style="text-align: center; margin: 20px 0;">
            <a href="https://secours73.fr/login" 
               style="background-color: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Accéder à la plateforme
            </a>
        </p>
    </body>
    </html>
    """
    
    success = await send_email(stagiaire_email, "Bienvenue sur la plateforme Secours 73", html_content)
    if success:
        return {"status": "success", "message": f"Email de bienvenue envoyé à {stagiaire_email}"}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de l'envoi de l'email")


async def send_welcome_email_internal(stagiaire_email: str, stagiaire_prenom: str):
    """Internal function to send welcome email (used during registration)"""
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #dc2626;">Bienvenue sur la plateforme de formation</h2>
        <p>Bonjour {stagiaire_prenom},</p>
        <p>Bienvenue sur la plateforme de formation ouverte à distance développée par <strong>Secours Alpes 73</strong>.</p>
        <p>Nous sommes ravis de vous accueillir pour cette première partie de votre formation.</p>
        <p>Cette plateforme a été conçue pour vous permettre d'apprendre à votre rythme et d'accéder facilement aux ressources pédagogiques mises à votre disposition.</p>
        <p>L'ensemble de l'équipe pédagogique vous souhaite une excellente formation et reste à votre disposition pour répondre à toutes vos questions ou vous accompagner si nécessaire.</p>
        <p style="margin-top: 30px;">Bonne formation et à très bientôt sur la plateforme.</p>
        <p style="margin-top: 30px;">Cordialement,</p>
        <p><strong>L'équipe pédagogique<br>Secours 73</strong></p>
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        <p style="text-align: center; margin: 20px 0;">
            <a href="https://secours73.fr/login" 
               style="background-color: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Accéder à la plateforme
            </a>
        </p>
    </body>
    </html>
    """
    
    await send_email(stagiaire_email, "Bienvenue sur la plateforme Secours 73", html_content)


@api_router.post("/formateur/send-email")
async def formateur_send_email(
    token: str = Query(...),
    to_email: str = Query(...),
    subject: str = Query(...),
    message: str = Query(...)
):
    """Formateur sends an email to a trainee"""
    formateur = await require_formateur(token)
    
    # Verify recipient exists and formateur has access
    recipient = await db.users.find_one({"email": to_email}, {"_id": 0})
    if not recipient:
        raise HTTPException(status_code=404, detail="Destinataire non trouvé")
    
    # Check if formateur has access to this user
    if recipient["role"] == "stagiaire" and recipient.get("groupe_id"):
        groupe = await db.groupes_formation.find_one({"id": recipient["groupe_id"]}, {"_id": 0})
        if groupe and groupe["formateur_id"] != formateur["id"] and formateur["id"] not in groupe.get("collaborateurs", []):
            raise HTTPException(status_code=403, detail="Vous n'avez pas accès à ce stagiaire")
    
    # Create HTML email
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #dc2626;">{subject}</h2>
        <div style="margin: 20px 0; line-height: 1.6;">
            {message.replace(chr(10), '<br>')}
        </div>
        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
        <p style="color: #666; font-size: 14px;">
            Message envoyé par <strong>{formateur['prenom']} {formateur['nom']}</strong><br>
            Formateur - Secours 73
        </p>
        <p style="text-align: center; margin: 20px 0;">
            <a href="https://secours73.fr/login" 
               style="background-color: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                Accéder à la plateforme
            </a>
        </p>
    </body>
    </html>
    """
    
    success = await send_email(to_email, subject, html_content)
    if success:
        return {"status": "success", "message": f"Email envoyé à {to_email}"}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de l'envoi de l'email")


# ============== DOCUMENT MANAGEMENT ==============

UPLOAD_DIR = Path("/app/uploads/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@api_router.post("/formateur/document/upload")
async def upload_document(
    token: str = Query(...),
    file: UploadFile = File(...),
    titre: str = Query(...),
    categorie: str = Query(...),
    description: Optional[str] = Query(None),
    destinataire_type: str = Query(...),  # "groupe" ou "stagiaire"
    groupe_id: Optional[str] = Query(None),
    stagiaire_id: Optional[str] = Query(None)
):
    """Upload a document for a group or specific trainee"""
    formateur = await require_formateur(token)
    
    # Validation
    if destinataire_type not in ["groupe", "stagiaire"]:
        raise HTTPException(status_code=400, detail="Type de destinataire invalide")
    
    if destinataire_type == "groupe" and not groupe_id:
        raise HTTPException(status_code=400, detail="groupe_id requis pour destinataire_type=groupe")
    
    if destinataire_type == "stagiaire" and not stagiaire_id:
        raise HTTPException(status_code=400, detail="stagiaire_id requis pour destinataire_type=stagiaire")
    
    # Verify formateur has access to the group/stagiaire
    if destinataire_type == "groupe":
        groupe = await db.groupes_formation.find_one({"id": groupe_id}, {"_id": 0})
        if not groupe:
            raise HTTPException(status_code=404, detail="Groupe non trouvé")
        if groupe["formateur_id"] != formateur["id"] and formateur["id"] not in groupe.get("collaborateurs", []):
            raise HTTPException(status_code=403, detail="Accès interdit à ce groupe")
    
    if destinataire_type == "stagiaire":
        stagiaire = await db.users.find_one({"id": stagiaire_id, "role": "stagiaire"}, {"_id": 0})
        if not stagiaire:
            raise HTTPException(status_code=404, detail="Stagiaire non trouvé")
        # Verify formateur has access to this stagiaire's group
        if stagiaire.get("groupe_id"):
            groupe = await db.groupes_formation.find_one({"id": stagiaire["groupe_id"]}, {"_id": 0})
            if groupe and groupe["formateur_id"] != formateur["id"] and formateur["id"] not in groupe.get("collaborateurs", []):
                raise HTTPException(status_code=403, detail="Accès interdit à ce stagiaire")
    
    # Save file
    doc_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix
    safe_filename = f"{doc_id}{file_ext}"
    file_path = UPLOAD_DIR / safe_filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'upload: {str(e)}")
    
    # Get file size
    file_size = file_path.stat().st_size
    
    # Save metadata to DB
    document = {
        "id": doc_id,
        "titre": titre,
        "categorie": categorie,
        "description": description,
        "filename": safe_filename,
        "original_filename": file.filename,
        "file_size": file_size,
        "formateur_id": formateur["id"],
        "formateur_nom": f"{formateur['prenom']} {formateur['nom']}",
        "destinataire_type": destinataire_type,
        "groupe_id": groupe_id if destinataire_type == "groupe" else None,
        "stagiaire_id": stagiaire_id if destinataire_type == "stagiaire" else None,
        "uploaded_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.documents.insert_one(document)
    
    return {
        "status": "success",
        "message": "Document uploadé avec succès",
        "document_id": doc_id
    }


@api_router.get("/stagiaire/documents")
async def get_stagiaire_documents(token: str = Query(...)):
    """Get all documents for a trainee"""
    stagiaire = await require_stagiaire(token)
    
    # Find documents for this stagiaire (direct or via group)
    query = {
        "$or": [
            {"stagiaire_id": stagiaire["id"]},
            {"groupe_id": stagiaire.get("groupe_id")}
        ]
    }
    
    documents = await db.documents.find(query, {"_id": 0}).to_list(1000)
    
    # Sort by category and date
    documents.sort(key=lambda x: (x["categorie"], x["uploaded_at"]), reverse=True)
    
    return documents


@api_router.get("/formateur/documents")
async def get_formateur_documents(token: str = Query(...)):
    """Get all documents uploaded by formateur"""
    formateur = await require_formateur(token)
    
    documents = await db.documents.find({"formateur_id": formateur["id"]}, {"_id": 0}).to_list(1000)
    documents.sort(key=lambda x: x["uploaded_at"], reverse=True)
    
    return documents


@api_router.get("/documents/{doc_id}/download")
async def download_document(doc_id: str, token: str = Query(...)):
    """Download a document"""
    user = await require_auth(token)
    
    # Find document
    document = await db.documents.find_one({"id": doc_id}, {"_id": 0})
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    
    # Check access rights
    if user["role"] == "stagiaire":
        # Stagiaire can access if document is for them or their group
        if document["destinataire_type"] == "stagiaire" and document["stagiaire_id"] != user["id"]:
            raise HTTPException(status_code=403, detail="Accès interdit")
        if document["destinataire_type"] == "groupe" and document["groupe_id"] != user.get("groupe_id"):
            raise HTTPException(status_code=403, detail="Accès interdit")
    elif user["role"] in ["formateur", "admin"]:
        # Formateurs and admins can access their own documents or documents in their groups
        if user["role"] == "formateur" and document["formateur_id"] != user["id"]:
            # Check if formateur has access to the group
            if document["destinataire_type"] == "groupe":
                groupe = await db.groupes_formation.find_one({"id": document["groupe_id"]}, {"_id": 0})
                if groupe and groupe["formateur_id"] != user["id"] and user["id"] not in groupe.get("collaborateurs", []):
                    raise HTTPException(status_code=403, detail="Accès interdit")
    
    # Serve file
    file_path = UPLOAD_DIR / document["filename"]
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return FileResponse(
        path=file_path,
        filename=document["original_filename"],
        media_type="application/octet-stream"
    )


@api_router.delete("/formateur/document/{doc_id}")
async def delete_document(doc_id: str, token: str = Query(...)):
    """Delete a document"""
    formateur = await require_formateur(token)
    
    document = await db.documents.find_one({"id": doc_id}, {"_id": 0})
    if not document:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    
    # Only owner or admin can delete
    if document["formateur_id"] != formateur["id"] and formateur["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès interdit")
    
    # Delete file
    file_path = UPLOAD_DIR / document["filename"]
    if file_path.exists():
        file_path.unlink()
    
    # Delete metadata
    await db.documents.delete_one({"id": doc_id})
    
    return {"status": "success", "message": "Document supprimé"}


# ============== ROOT API ==============

@api_router.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API Secours 73",
        "developpe_par": "Secours Alpes 73",
        "description": "Association habilitée pour la formation aux premiers secours"
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
