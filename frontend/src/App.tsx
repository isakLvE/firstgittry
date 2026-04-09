import React from 'react'
import { Button, Card, Typography } from 'antd'

const { Title, Paragraph } = Typography

function App() {
  return (
    <div style={{ padding: '24px', maxWidth: '800px', margin: '0 auto' }}>
      <Card>
        <Title level={2}>校园问答智能体</Title>
        <Paragraph>基于RAG技术的校园问答系统</Paragraph>
        <Button type="primary" onClick={() => alert('功能开发中')}>
          开始使用
        </Button>
      </Card>
    </div>
  )
}

export default App
