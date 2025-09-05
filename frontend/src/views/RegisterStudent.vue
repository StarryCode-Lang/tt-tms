<!-- 学员注册 -->
<template>
  <el-form :model="form" label-width="120px">
    <!-- 字段 -->
    <el-button type="primary" @click="register">注册</el-button>
  </el-form>
</template>

<script setup>
import { reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = reactive({ /* 字段 */ })

const register = async () => {
  await axios.post('/api/register/student', form)
  router.push('/login')
}
</script>