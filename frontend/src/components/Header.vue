<!-- 头部导航 -->
<template>
  <el-menu mode="horizontal">
    <el-menu-item index="1">首页</el-menu-item>
    <el-menu-item v-if="role === 'super_admin'" index="2" @click="$router.push('/campus')">校区管理</el-menu-item>
    <el-menu-item index="3" @click="$router.push('/profile')">个人资料</el-menu-item>
    <el-menu-item index="4" @click="logout">登出</el-menu-item>
  </el-menu>
</template>

<script setup>
import { useAuthStore } from '../store'
import { useRouter } from 'vue-router'

const store = useAuthStore()
const router = useRouter()
const role = store.role

const logout = async () => {
  // 调用 /api/logout
  store.logout()
  router.push('/login')
}
</script>