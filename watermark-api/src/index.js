/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

export default {
  async fetch(request, env) {
    // 处理 CORS 预检请求
    if (request.method === 'OPTIONS') {
      return handleOptions(request)
    }

    // 处理文件上传请求
    if (request.method === 'POST' && new URL(request.url).pathname === '/process') {
      return handleProcess(request)
    }

    return new Response('API is running', {
      headers: corsHeaders
    })
  }
}

// CORS 头部配置
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
}

async function handleProcess(request) {
  try {
    const formData = await request.formData()
    const file = formData.get('file')
    
    if (!file) {
      return new Response('No file uploaded', { 
        status: 400,
        headers: corsHeaders
      })
    }

    // TODO: 实现文件处理逻辑
    // 目前返回测试响应
    return new Response('File processed successfully', {
      headers: corsHeaders
    })
  } catch (err) {
    return new Response(`Error: ${err.message}`, { 
      status: 500,
      headers: corsHeaders
    })
  }
}

function handleOptions(request) {
  return new Response(null, {
    headers: corsHeaders
  })
}
