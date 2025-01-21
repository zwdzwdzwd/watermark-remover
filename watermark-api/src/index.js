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
    if (request.method === 'OPTIONS') {
      return handleOptions(request)
    }

    if (request.method === 'POST' && new URL(request.url).pathname === '/process') {
      return handleProcess(request)
    }

    return new Response('API is running', {
      headers: corsHeaders
    })
  }
}

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
      return new Response('No file uploaded', { status: 400, headers: corsHeaders })
    }

    const fileData = await file.arrayBuffer()
    const fileType = file.type

    // 处理图片文件
    if (fileType.startsWith('image/')) {
      // 直接返回原始图片作为测试
      return new Response(fileData, {
        headers: {
          ...corsHeaders,
          'Content-Type': fileType,
          'Content-Disposition': `attachment; filename="processed_${file.name}"`
        }
      })
    }

    // 其他文件类型暂时返回原文件
    return new Response(fileData, {
      headers: {
        ...corsHeaders,
        'Content-Type': fileType,
        'Content-Disposition': `attachment; filename="processed_${file.name}"`
      }
    })
  } catch (err) {
    console.error('Error:', err)
    return new Response(`Error: ${err.message}`, { status: 500, headers: corsHeaders })
  }
}

function handleOptions(request) {
  return new Response(null, { headers: corsHeaders })
}
