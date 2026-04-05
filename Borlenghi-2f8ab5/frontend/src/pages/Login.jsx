import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import useStore from '../store/useStore'
import { login } from '../services/noteService'
import { useState } from 'react'

function Login() {
  const { register, handleSubmit, formState: { errors } } = useForm()
  const setToken = useStore((s) => s.setToken)
  const navigate = useNavigate()
  const [error, setError] = useState('')

  const onSubmit = async (data) => {
    try {
      setError('')
      const result = await login(data.username, data.password)
      // IMPORTANT: sync both store AND localStorage
      localStorage.setItem('token', result.access_token)
      setToken(result.access_token)
      navigate('/notes')
    } catch (err) {
      setError('Invalid username or password')
    }
  }

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit(onSubmit)}>
        <h1>Notes App</h1>
        <p>Sign in to continue</p>

        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            {...register('username', { required: 'Username is required' })}
            placeholder="admin"
          />
          {errors.username && <span className="error">{errors.username.message}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            {...register('password', { required: 'Password is required' })}
            placeholder="admin"
          />
          {errors.password && <span className="error">{errors.password.message}</span>}
        </div>

        {error && <div className="error-message">{error}</div>}

        <button type="submit">Sign In</button>
      </form>
    </div>
  )
}

export default Login
