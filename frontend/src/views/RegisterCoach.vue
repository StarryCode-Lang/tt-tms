<!-- 教练注册 -->
<template>
  <el-form :model="form" label-width="120px">
    <el-form-item label="用户名">
      <el-input v-model="form.username" />
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="form.password" type="password" />
    </el-form-item>
    <el-form-item label="姓名">
      <el-input v-model="form.name" />
    </el-form-item>
    <el-button type="primary" @click="register">注册</el-button>
  </el-form>
</template>

<script setup>
import { reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = reactive({
  username: '',
  password: '',
  name: ''
})

const register = async () => {
  try {
    await axios.post('/api/register/coach', form)
    router.push('/login')
  } catch (err) {
    console.error('Register error:', err)
  }
}
</script>
