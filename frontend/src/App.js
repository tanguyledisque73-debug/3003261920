import React from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "./components/ui/sonner";

// Pages
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import RegisterVisiteur from "./pages/RegisterVisiteur";
import SetPassword from "./pages/SetPassword";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import Messages from "./pages/Messages";

// Stagiaire Pages
import StagiaireDashboard from "./pages/stagiaire/Dashboard";
import StagiaireChapitres from "./pages/stagiaire/Chapitres";
import StagiaireChapterDetail from "./pages/stagiaire/ChapterDetail";
import StagiaireQuiz from "./pages/stagiaire/Quiz";
import StagiaireDocuments from "./pages/stagiaire/Documents";

// Formateur Pages
import FormateurDashboard from "./pages/formateur/Dashboard";
import FormateurGroupes from "./pages/formateur/Groupes";
import FormateurGroupeDetail from "./pages/formateur/GroupeDetail";
import FormateurStagiaireDetail from "./pages/formateur/StagiaireDetail";
import FormateurDocuments from "./pages/formateur/Documents";
import FormateurSendEmail from "./pages/formateur/SendEmail";
import FormateurGroupeSettings from "./pages/formateur/GroupeSettings";

// Admin Pages
import AdminDashboard from "./pages/admin/Dashboard";
import AdminFormateurs from "./pages/admin/Formateurs";
import AdminQuizzes from "./pages/admin/Quizzes";
import AdminQuizEditor from "./pages/admin/QuizEditor";
import AdminChapters from "./pages/admin/Chapters";
import AdminChapterEditor from "./pages/admin/ChapterEditor";
import AdminSettings from "./pages/admin/Settings";
import AdminCustomization from "./pages/admin/Customization";

// Visiteur Pages
import VisiteurDashboard from "./pages/visiteur/Dashboard";

// Public Pages
import PSCChapters from "./pages/public/PSCChapters";
import PSCChapterDetail from "./pages/public/PSCChapterDetail";
import ChaptersPreview from "./pages/public/ChaptersPreview";
import PSEInfo from "./pages/public/PSEInfo";
import BNSSAInfo from "./pages/public/BNSSAInfo";
import HelpPage from "./pages/Help";

// Auth helper
import { getUser } from "./lib/api";

// Protected Route Component
const ProtectedRoute = ({ children, allowedRoles }) => {
  const user = getUser();
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  // Check if user needs to set password
  if (user.must_set_password) {
    return <Navigate to="/set-password" replace />;
  }
  
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    // Redirect based on role
    switch (user.role) {
      case 'admin':
        return <Navigate to="/admin" replace />;
      case 'formateur':
        return <Navigate to="/formateur" replace />;
      case 'stagiaire':
        return <Navigate to="/stagiaire" replace />;
      case 'visiteur':
        return <Navigate to="/visiteur" replace />;
      default:
        return <Navigate to="/" replace />;
    }
  }
  
  return children;
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/inscription-gratuite" element={<RegisterVisiteur />} />
          <Route path="/set-password" element={<SetPassword />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/psc" element={<PSCChapters />} />
          <Route path="/psc/chapitre/:chapterId" element={<PSCChapterDetail />} />
          <Route path="/pse-info" element={<PSEInfo />} />
          <Route path="/bnssa-info" element={<BNSSAInfo />} />
          <Route path="/decouvrir" element={<ChaptersPreview />} />
          <Route path="/aide" element={<HelpPage />} />
          
          {/* Messages (accessible à tous les utilisateurs connectés) */}
          <Route 
            path="/messages" 
            element={
              <ProtectedRoute allowedRoles={["stagiaire", "formateur", "admin", "visiteur"]}>
                <Messages />
              </ProtectedRoute>
            } 
          />
          
          {/* Stagiaire Routes */}
          <Route 
            path="/stagiaire" 
            element={
              <ProtectedRoute allowedRoles={["stagiaire"]}>
                <StagiaireDashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/stagiaire/chapitres" 
            element={
              <ProtectedRoute allowedRoles={["stagiaire"]}>
                <StagiaireChapitres />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/stagiaire/chapitre/:chapterId" 
            element={
              <ProtectedRoute allowedRoles={["stagiaire"]}>
                <StagiaireChapterDetail />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/stagiaire/quiz/:chapterId" 
            element={
              <ProtectedRoute allowedRoles={["stagiaire"]}>
                <StagiaireQuiz />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/stagiaire/documents" 
            element={
              <ProtectedRoute allowedRoles={["stagiaire"]}>
                <StagiaireDocuments />
              </ProtectedRoute>
            } 
          />
          
          {/* Formateur Routes */}
          <Route 
            path="/formateur" 
            element={
              <ProtectedRoute allowedRoles={["formateur"]}>
                <FormateurDashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/formateur/groupes" 
            element={
              <ProtectedRoute allowedRoles={["formateur"]}>
                <FormateurGroupes />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/formateur/groupe/:groupeId" 
            element={
              <ProtectedRoute allowedRoles={["formateur"]}>
                <FormateurGroupeDetail />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/formateur/stagiaire/:stagiaireId" 
            element={
              <ProtectedRoute allowedRoles={["formateur"]}>
                <FormateurStagiaireDetail />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/formateur/documents" 
            element={
              <ProtectedRoute allowedRoles={["formateur"]}>
                <FormateurDocuments />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/formateur/send-email" 
            element={
              <ProtectedRoute allowedRoles={["formateur"]}>
                <FormateurSendEmail />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/formateur/groupe/:groupeId/settings" 
            element={
              <ProtectedRoute allowedRoles={["formateur"]}>
                <FormateurGroupeSettings />
              </ProtectedRoute>
            } 
          />
          
          {/* Admin Routes */}
          <Route 
            path="/admin" 
            element={
              <ProtectedRoute allowedRoles={["admin"]}>
                <AdminDashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/formateurs" 
            element={
              <ProtectedRoute allowedRoles={["admin"]}>
                <AdminFormateurs />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/quizzes" 
            element={
              <ProtectedRoute allowedRoles={["admin"]}>
                <AdminQuizzes />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/quiz/:quizId?" 
            element={
              <ProtectedRoute allowedRoles={["admin"]}>
                <AdminQuizEditor />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/chapters" 
            element={
              <ProtectedRoute allowedRoles={["admin"]}>
                <AdminChapters />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/chapter/:chapterId?" 
            element={
              <ProtectedRoute allowedRoles={["admin"]}>
                <AdminChapterEditor />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/settings" 
            element={
              <ProtectedRoute allowedRoles={["admin"]}>
                <AdminSettings />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/customization" 
            element={
              <ProtectedRoute allowedRoles={["admin"]}>
                <AdminCustomization />
              </ProtectedRoute>
            } 
          />
          
          {/* Visiteur Routes */}
          <Route 
            path="/visiteur" 
            element={
              <ProtectedRoute allowedRoles={["visiteur"]}>
                <VisiteurDashboard />
              </ProtectedRoute>
            } 
          />
          
          {/* Legacy redirects */}
          <Route path="/dashboard" element={<Navigate to="/stagiaire" replace />} />
          <Route path="/chapitres" element={<Navigate to="/decouvrir" replace />} />
          
          {/* Catch all - redirect to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" richColors />
    </div>
  );
}

export default App;
