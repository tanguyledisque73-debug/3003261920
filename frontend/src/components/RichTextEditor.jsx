import React, { useMemo } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import './RichTextEditor.css';

/**
 * Composant éditeur de texte riche réutilisable
 * Utilisable partout sur le site pour l'édition de contenu
 */
const RichTextEditor = ({ 
    value, 
    onChange, 
    placeholder = "Commencez à écrire...",
    height = "300px",
    readOnly = false,
    minimal = false
}) => {
    // Configuration des outils de la barre d'outils
    const modules = useMemo(() => {
        if (minimal) {
            // Version minimale pour les petits champs
            return {
                toolbar: [
                    ['bold', 'italic', 'underline'],
                    [{ 'color': [] }],
                    ['clean']
                ]
            };
        }
        
        // Version complète type Word
        return {
            toolbar: [
                // Formatage de texte
                [{ 'header': [1, 2, 3, false] }],
                [{ 'font': [] }],
                [{ 'size': ['small', false, 'large', 'huge'] }],
                
                // Style de texte
                ['bold', 'italic', 'underline', 'strike'],
                [{ 'color': [] }, { 'background': [] }],
                
                // Alignement
                [{ 'align': [] }],
                
                // Listes
                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                [{ 'indent': '-1'}, { 'indent': '+1' }],
                
                // Autres
                ['blockquote', 'code-block'],
                ['link', 'image'],
                
                // Nettoyage
                ['clean']
            ]
        };
    }, [minimal]);

    // Formats autorisés
    const formats = [
        'header', 'font', 'size',
        'bold', 'italic', 'underline', 'strike',
        'color', 'background',
        'align',
        'list', 'bullet', 'indent',
        'blockquote', 'code-block',
        'link', 'image'
    ];

    return (
        <div className={`rich-text-editor ${readOnly ? 'read-only' : ''}`}>
            <ReactQuill
                theme="snow"
                value={value || ''}
                onChange={onChange}
                modules={modules}
                formats={formats}
                placeholder={placeholder}
                readOnly={readOnly}
                style={{ height }}
            />
        </div>
    );
};

export default RichTextEditor;
