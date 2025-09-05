<!-- 仪表盘（根据角色显示） -->
<template>
  <div>
    <h1>仪表盘</h1>
    <p>欢迎来到 TT-TMS 系统</p>
    <p>当前角色: {{ role }}</p>
  </div>
</template>

<script setup>
import { useAuthStore } from '../store'

const store = useAuthStore()
const role = store.role
</script>
