<template>
  <tr class="submission-record">
    <td>{{ record.submissionTime | formatDate }}</td>
    <td>{{ record.problemId }}</td>
    <td>{{ record.submissionContent }}</td>
    <td>{{ record.result }}</td>
  </tr>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/student/Navbar.vue';
export default {
  name: "SubmissionRecord",
  props: {
    record: Object
  },
  filters: {
    formatDate(value) {
      return new Date(value).toLocaleString();
    }
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

td {
  border: 1px solid #ccc;
  padding: 10px;
}

/* 可添加表格标题样式 */
th {
  background-color: #f4f4f4;
  padding: 10px;
  border: 1px solid #ccc;
}
</style>