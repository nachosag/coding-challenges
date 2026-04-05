import { Navigate } from 'react-router-dom'
import useStore from '../store/useStore'

function ProtectedRoute({ children }) {
  const token = useStore((s) => s.token)
  if (!token) {
    return <Navigate to="/login" replace />
  }
  return children
}

export default ProtectedRoute
