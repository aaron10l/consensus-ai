import { useState } from 'react'
import TextBox from './components/TextBox'
import './App.css'

const App = () => {
  const [chatHistory, setChatHistory] = useState([]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>consensus.ai</h1>
      </header>
      <main>
        <TextBox chatHistory={chatHistory} setChatHistory={setChatHistory} />
      </main>
    </div>
  )
}

export default App
