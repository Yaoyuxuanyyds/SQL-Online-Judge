import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'

// Admin
import QuestionManage from "@/components/admin/QuestionManage"
import TableManage from "@/components/admin/TableManage"
import AnswerManage from "@/components/admin/AnswerManage"
import StudentManage from '@/components/admin/StudentManage'
import AdminHome from '@/components/admin/Index'

// Teacher
import TeacherHome from '@/components/teacher/Index'
import ImportQuestions from '@/components/teacher/ImportQuestions.vue'
import CreateExam from '@/components/teacher/CreateExam.vue'

// Student
import StudentHome from '@/components/student/Index'
import Submit from '@/components/student/Submit'
import Question from "@/components/student/Question"
import AnswerQuestion from './components/student/AnswerQuestion.vue'
import Contest from "@/components/student/Contest"
import Community from "@/components/Community"

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/community',
      name: 'community',
      component: Community
    },
    {
      path: '/admin',
      name: 'admin/index',
      component: AdminHome,
      children: [
        {
          path: 'StudentManage',
          component: StudentManage
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
      name: 'student',
      component: StudentHome,
    },
    {
      path: '/student/submit',
      name: 'submit',
      component: Submit
    },
    {
      path: '/student/contest',
      name: 'contest',
      component: Contest
    },
    {
      path: '/student/question',
      name: 'question',
      component: Question
    },
    {
      path: '/student/answer_question/:id',
      name: 'answer-question',
      component: AnswerQuestion
    }

  ]
})
