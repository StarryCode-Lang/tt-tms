<!-- 登录页 -->
<template>
  <el-form :model="form" label-width="120px">
    <el-form-item label="用户名">
      <el-input v-model="form.username" />
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="form.password" type="password" />
    </el-form-item>
    <el-button type="primary" @click="login">登录</el-button>
  </el-form>
</template>

<script setup>
import { reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store'

const router = useRouter()
const store = useAuthStore()
const form = reactive({ username: '', password: '' })

const login = async () => {
  try {
    const res = await axios.post('/api/login', form, {
      headers: { 'Content-Type': 'application/json' }
    })
    console.log('Login response:', res.data)
    store.setToken(res.data.token, 'student') // 实际应从 JWT 解析 role
    router.push('/dashboard')
  } catch (err) {
    console.error('Login error:', err.response ? err.response.data : err.message)
  }
}
</script>