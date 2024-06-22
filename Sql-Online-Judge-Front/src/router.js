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
import Submit_t from '@/components/teacher/Submit'
import Question_t from "@/components/teacher/Question"
import AnswerQuestion_t from '@/components/teacher/AnswerQuestion.vue'
import Contest_t from "@/components/teacher/Contest"
import Community_t from "@/components/teacher/Community"


// Student
import StudentHome from '@/components/student/Index'
import Submit from '@/components/student/Submit'
import Question from "@/components/student/Question"
import AnswerQuestion from '@/components/student/AnswerQuestion.vue'
import Contest from "@/components/student/Contest"
import Question_contest from "@/components/student/Question_contest"
import AnswerQuestion_contest from '@/components/student/AnswerQuestion_contest.vue'
import Community from "@/components/student/Community"


Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
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
      name: 'teacher',
      component: TeacherHome,
    },
    {
      path: '/teacher/import',
      name: 'import',
      component: ImportQuestions
    },
    {
      path: '/teacher/create',
      name: 'create',
      component: CreateExam
    },
    {
      path: '/teacher/submit',
      name: 'submit_t',
      component: Submit_t
    },
    {
      path: '/teacher/contest',
      name: 'contest_t',
      component: Contest_t
    },
    {
      path: '/teacher/question',
      name: 'question_t',
      component: Question_t
    },
    {
      path: '/teacher/question/:id',
      name: 'answer-question_t',
      component: AnswerQuestion_t
    },
    {
      path: '/teacher/community',
      name: 'community_t',
      component: Community_t
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
      path: '/student/question',
      name: 'question',
      component: Question
    },
    {
      path: '/student/question/:id',
      name: 'answer-question',
      component: AnswerQuestion
    },
    {
      path: '/student/contest',
      name: 'contest',
      component: Contest
    },
    {
      path: '/student/contest/:id',
      name: 'question_contest',
      component: Question_contest
    },
    {
      path: '/student/contest/:id/answer',
      name: 'answer-question_contest',
      component: AnswerQuestion_contest
    },
    {
      path: '/student/community',
      name: 'community',
      component: Community
    },

  ]
})
