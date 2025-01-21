<template>
  <div class="container">
    <h1>水印去除工具</h1>
    <div class="upload-container">
      <form @submit.prevent="handleSubmit">
        <div class="file-input">
          <label for="file" class="button">选择文件</label>
          <input type="file" id="file" ref="fileInput" @change="handleFileChange" 
                 accept=".jpg,.jpeg,.png,.pdf,.doc,.docx" style="display: none">
          <p>{{ fileName || '未选择文件' }}</p>
        </div>
        <button type="submit" class="button" :disabled="!fileName || processing">
          {{ processing ? '处理中...' : '处理文件' }}
        </button>
      </form>
      
      <!-- 添加状态提示 -->
      <div v-if="processing" class="status">
        <div class="loading-spinner"></div>
        <p>正在处理文件，请稍候...</p>
        <p class="sub-text">处理时间取决于文件大小和页数</p>
      </div>
      
      <!-- 添加错误提示 -->
      <div v-if="error" class="error">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const fileName = ref('')
    const processing = ref(false)
    const error = ref('')
    const fileInput = ref(null)

    const handleFileChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        fileName.value = file.name
        error.value = '' // 清除之前的错误
      }
    }

    const handleSubmit = async () => {
      const file = fileInput.value.files[0]
      if (!file) return

      processing.value = true
      error.value = ''
      const formData = new FormData()
      formData.append('file', file)

      try {
        const response = await axios.post('http://127.0.0.1:8080/process', formData, {
          responseType: 'blob',
          timeout: 300000, // 设置超时时间为5分钟
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          withCredentials: false,
          maxContentLength: Infinity,
          maxBodyLength: Infinity
        })
        
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `processed_${file.name}`)
        document.body.appendChild(link)
        link.click()
        link.remove()
      } catch (err) {
        error.value = '处理失败，请重试。' + (err.response?.data || err.message || '网络错误')
        console.error('Error details:', err)
      }
    }

    return {
      fileName,
      processing,
      error,
      fileInput,
      handleFileChange,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.upload-container {
  border: 2px dashed #ccc;
  padding: 20px;
  text-align: center;
  margin: 20px 0;
}

.button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin: 10px;
}

.button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.status {
  margin-top: 20px;
  text-align: center;
  color: #666;
}

.sub-text {
  font-size: 0.9em;
  color: #999;
}

.error {
  margin-top: 20px;
  color: #ff4444;
  text-align: center;
}

.loading-spinner {
  display: inline-block;
  width: 30px;
  height: 30px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>