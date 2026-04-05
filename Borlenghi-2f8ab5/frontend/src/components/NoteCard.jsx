import styles from '../styles/NoteCard.module.css'

function NoteCard({ note, categories, onEdit, onDelete, onArchive }) {
  const category = categories.find((c) => c.id === note.category_id)

  return (
    <div className={`${styles.card} ${note.is_archived ? styles.archived : ''}`}>
      <div className={styles.header}>
        <h3 className={styles.title}>{note.title}</h3>
        {note.is_archived && <span className={styles.badge}>Archived</span>}
        {category && <span className={styles.category}>{category.name}</span>}
      </div>

      <p className={styles.content}>{note.content}</p>

      <div className={styles.actions}>
        <button onClick={onEdit} className={styles.btnEdit}>Edit</button>
        <button onClick={onArchive} className={styles.btnArchive}>
          {note.is_archived ? 'Unarchive' : 'Archive'}
        </button>
        <button onClick={onDelete} className={styles.btnDelete}>Delete</button>
      </div>
    </div>
  )
}

export default NoteCard
