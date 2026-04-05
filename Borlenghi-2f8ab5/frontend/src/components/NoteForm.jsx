import { useForm } from 'react-hook-form'
import { useEffect } from 'react'

function NoteForm({ note, categories, onSubmit, onCancel }) {
  const { register, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: note
      ? { title: note.title, content: note.content, category_id: note.category_id ?? '' }
      : { title: '', content: '', category_id: '' },
  })

  useEffect(() => {
    if (note) {
      reset({ title: note.title, content: note.content, category_id: note.category_id ?? '' })
    } else {
      reset({ title: '', content: '', category_id: '' })
    }
  }, [note, reset])

  const submitHandler = (data) => {
    onSubmit({
      title: data.title,
      content: data.content,
      category_id: data.category_id ? Number(data.category_id) : null,
    })
  }

  return (
    <div className="note-form-overlay">
      <form className="note-form" onSubmit={handleSubmit(submitHandler)}>
        <h2>{note ? 'Edit Note' : 'New Note'}</h2>

        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            id="title"
            type="text"
            {...register('title', { required: 'Title is required' })}
            placeholder="Note title"
          />
          {errors.title && <span className="error">{errors.title.message}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            {...register('content')}
            placeholder="Write your note..."
            rows={5}
          />
        </div>

        <div className="form-group">
          <label htmlFor="category_id">Category</label>
          <select id="category_id" {...register('category_id')}>
            <option value="">No category</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
        </div>

        <div className="form-actions">
          <button type="submit">{note ? 'Save Changes' : 'Create Note'}</button>
          <button type="button" onClick={onCancel} className="btn-cancel">Cancel</button>
        </div>
      </form>
    </div>
  )
}

export default NoteForm
