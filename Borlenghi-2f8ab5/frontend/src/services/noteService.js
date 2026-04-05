import api from './api'

export const getNotes = (archived = null, categoryId = null) => {
  const params = {}
  if (archived !== null) params.archived = archived
  if (categoryId !== null) params.category_id = categoryId
  return api.get('/notes', { params }).then((r) => r.data)
}

export const getNote = (id) => api.get(`/notes/${id}`).then((r) => r.data)

export const createNote = (data) => api.post('/notes', data).then((r) => r.data)

export const updateNote = (id, data) =>
  api.put(`/notes/${id}`, data).then((r) => r.data)

export const deleteNote = (id) => api.delete(`/notes/${id}`)

export const archiveNote = (id, isArchived) =>
  api.patch(`/notes/${id}/archive`, { is_archived: isArchived }).then((r) => r.data)

export const assignCategory = (id, categoryId) =>
  api.patch(`/notes/${id}/category`, { category_id: categoryId }).then((r) => r.data)

export const getCategories = () => api.get('/categories').then((r) => r.data)

export const login = (username, password) =>
  api.post('/auth/login', { username, password }).then((r) => r.data)