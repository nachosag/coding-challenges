import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import useStore from '../store/useStore'
import { getNotes, getCategories, deleteNote, archiveNote, createNote, updateNote, assignCategory } from '../services/noteService'
import NoteCard from '../components/NoteCard'
import NoteForm from '../components/NoteForm'

function NotesPage() {
  const {
    notes, setNotes, removeNote, updateNoteInStore, addNote,
    categories, setCategories,
    filterArchived, filterCategory,
    setFilterArchived, setFilterCategory,
    logout,
  } = useStore()

  const navigate = useNavigate()
  const [showForm, setShowForm] = useState(false)
  const [editingNote, setEditingNote] = useState(null)
  const [loading, setLoading] = useState(true)

  // Load notes and categories on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [notesData, catsData] = await Promise.all([
          getNotes(),
          getCategories(),
        ])
        setNotes(notesData)
        setCategories(catsData)
      } catch (err) {
        console.error('Failed to fetch data', err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  // Reload notes when filters change
  useEffect(() => {
    const fetchFiltered = async () => {
      try {
        const notesData = await getNotes(filterArchived, filterCategory)
        setNotes(notesData)
      } catch (err) {
        console.error('Failed to fetch notes', err)
      }
    }
    fetchFiltered()
  }, [filterArchived, filterCategory])

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this note?')) return
    try {
      await deleteNote(id)
      removeNote(id)
    } catch (err) {
      console.error('Failed to delete', err)
    }
  }

  const handleArchive = async (id, archived) => {
    try {
      const updated = await archiveNote(id, archived)
      updateNoteInStore(updated)
    } catch (err) {
      console.error('Failed to archive', err)
    }
  }

  const handleCreate = async (data) => {
    try {
      const newNote = await createNote(data)
      addNote(newNote)
      setShowForm(false)
    } catch (err) {
      console.error('Failed to create', err)
    }
  }

  const handleUpdate = async (data) => {
    try {
      let updated = await updateNote(editingNote.id, data)
      // Update category separately if changed
      if (data.category_id !== editingNote.category_id) {
        updated = await assignCategory(editingNote.id, data.category_id)
      }
      updateNoteInStore(updated)
      setEditingNote(null)
      setShowForm(false)
    } catch (err) {
      console.error('Failed to update', err)
    }
  }

  const handleEdit = (note) => {
    setEditingNote(note)
    setShowForm(true)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    logout()
    navigate('/login')
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div className="notes-container">
      <header className="notes-header">
        <h1>My Notes</h1>
        <div className="header-actions">
          <button onClick={() => { setEditingNote(null); setShowForm(true) }}>+ New Note</button>
          <button onClick={handleLogout} className="btn-logout">Logout</button>
        </div>
      </header>

      <div className="filters">
        <div className="filter-group">
          <label>Show:</label>
          <select
            value={filterArchived === null ? 'all' : filterArchived ? 'archived' : 'active'}
            onChange={(e) => {
              const val = e.target.value
              setFilterArchived(val === 'all' ? null : val === 'archived')
            }}
          >
            <option value="all">All Notes</option>
            <option value="active">Active</option>
            <option value="archived">Archived</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Category:</label>
          <select
            value={filterCategory ?? ''}
            onChange={(e) => setFilterCategory(e.target.value ? Number(e.target.value) : null)}
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
        </div>
      </div>

      {showForm && (
        <NoteForm
          note={editingNote}
          categories={categories}
          onSubmit={editingNote ? handleUpdate : handleCreate}
          onCancel={() => { setShowForm(false); setEditingNote(null) }}
        />
      )}

      <div className="notes-list">
        {notes.length === 0 ? (
          <p className="empty-state">No notes found. Create one!</p>
        ) : (
          notes.map((note) => (
            <NoteCard
              key={note.id}
              note={note}
              categories={categories}
              onEdit={() => handleEdit(note)}
              onDelete={() => handleDelete(note.id)}
              onArchive={() => handleArchive(note.id, !note.is_archived)}
            />
          ))
        )}
      </div>
    </div>
  )
}

export default NotesPage
