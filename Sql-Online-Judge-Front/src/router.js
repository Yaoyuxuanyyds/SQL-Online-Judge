import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import StudentHome from '@/components/student/Index'
import Submit from '@/components/student/Submit'
import Statistics from '@/components/student/Statistics'
import AdminHome from '@/components/admin/Index'
import TeacherHome from '@/components/teacher/Index' // 新增老师首页组件
import StudentManage from '@/components/admin/StudentManage'
import Question from "@/components/student/Question"
import DatabaseManage from "@/components/admin/DatabaseManage"
import QuestionManage from "@/components/admin/QuestionManage"
import TableManage from "@/components/admin/TableManage"
import AnswerManage from "@/components/admin/AnswerManage"
import Register from '@/components/Register' // 新增注册组件
import ImportQuestions from '@/components/teacher/ImportQuestions.vue' // 导入题目组件
import CreateExam from '@/components/teacher/CreateExam.vue' // 发起竞赛组件

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/admin',
      name: 'admin/index',
      component: AdminHome,
      children:[
        {
          path: 'StudentManage',
          component: StudentManage
        },
        {
          path: 'DatabaseManage',
          component: DatabaseManage
        },
        {
          path: 'QuestionManage',
          component: QuestionManage
        },
        {
          path: 'TableManage',
          component: TableManage,
          name: 'TableManage'
        },
        {
          path: 'AnswerManage',
          component: AnswerManage,
          name: 'AnswerManage'
        }
      ]
    },
    {
      path: '/teacher',
      name: 'teacher/index',
      component: TeacherHome,
      children: [
        {
          path: 'import',
          component: ImportQuestions
        },
        {
          path: 'create-exam',
          component: CreateExam
        }
      ]
    },
    {
      path: '/student',
      name: 'student/index',
      component: StudentHome,
      children:[
        {
          path: 'Submit',
          component: Submit
        },
        {
          path: 'Statistics',
          component: Statistics
        },
        {
          path: 'Question',
          component: Question,
          name: 'Question'
        }
      ]
    },
    {
      path: '/register', // 注册页面路由
      name: 'register',
      component: Register
    }
  ]
})
