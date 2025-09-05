<!-- 根组件 -->
<template>
  <el-container>
    <el-header><Header v-if="route.path !== '/login'" /></el-header>
    <el-main><router-view /></el-main>
  </el-container>
</template>

<script setup>
import { useRoute } from 'vue-router'
import Header from './components/Header.vue'

const route = useRoute()
</script>