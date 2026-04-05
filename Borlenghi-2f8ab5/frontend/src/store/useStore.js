import { create } from 'zustand'

const useStore = create((set, get) => ({
  // Auth
  token: null,
  setToken: (token) => set({ token }),
  logout: () => set({ token: null, notes: [], categories: [] }),

  // Notes
  notes: [],
  setNotes: (notes) => set({ notes }),
  addNote: (note) => set((s) => ({ notes: [...s.notes, note] })),
  updateNoteInStore: (note) =>
    set((s) => ({ notes: s.notes.map((n) => (n.id === note.id ? note : n)) })),
  removeNote: (id) =>
    set((s) => ({ notes: s.notes.filter((n) => n.id !== id) })),

  // Categories
  categories: [],
  setCategories: (categories) => set({ categories }),

  // Filters
  filterArchived: null, // null = all, true = archived, false = active
  filterCategory: null,
  setFilterArchived: (val) => set({ filterArchived: val }),
  setFilterCategory: (val) => set({ filterCategory: val }),
}))

export default useStore