import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ComponentName from './ComponentName'

describe('ComponentName', () => {
  it('renders correctly', () => {
    render(<ComponentName />)
    expect(screen.getByRole('heading')).toBeInTheDocument()
  })

  it('handles user interaction', async () => {
    const user = userEvent.setup()
    render(<ComponentName />)

    const button = screen.getByRole('button', { name: /click me/i })
    await user.click(button)

    expect(screen.getByText(/clicked/i)).toBeInTheDocument()
  })

  it('displays correct text with props', () => {
    const testProp = 'Test Value'
    render(<ComponentName value={testProp} />)

    expect(screen.getByText(testProp)).toBeInTheDocument()
  })

  it('handles async data loading', async () => {
    render(<ComponentName />)

    // Wait for loading to finish
    expect(screen.getByText(/loading/i)).toBeInTheDocument()

    // Wait for data to appear
    const data = await screen.findByText(/data loaded/i)
    expect(data).toBeInTheDocument()
  })

  it('calls callback function when triggered', async () => {
    const user = userEvent.setup()
    const mockCallback = vi.fn()

    render(<ComponentName onAction={mockCallback} />)

    const button = screen.getByRole('button')
    await user.click(button)

    expect(mockCallback).toHaveBeenCalledTimes(1)
  })
})
