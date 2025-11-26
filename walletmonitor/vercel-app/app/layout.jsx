import './globals.css'
import Navigation from '../components/Navigation'

export const metadata = {
  title: 'Flow Monitor',
  description: '基于TradingView Lightweight Charts的资金进出情况展示工具',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en-US">
      <body>
        <Navigation />
        {children}
      </body>
    </html>
  )
} 