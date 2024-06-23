import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'

// Admin
import ManageUsers from '@/components/admin/ManageUsers'

// Teacher
import TeacherHome from '@/components/teacher/Index'
import ImportQuestions from '@/components/teacher/ImportQuestions.vue'
import CreateExam from '@/components/teacher/CreateExam.vue'
import Submit_t from '@/components/teacher/Submit'
import Question_t from "@/components/teacher/Question"
import AnswerQuestion_t from '@/components/teacher/AnswerQuestion.vue'
import Contest_t from "@/components/teacher/Contest"
import Community_t from "@/components/teacher/Community"
import ArticleEditor_t from "@/components/student/ArticleEditor"

// Student
import StudentHome from '@/components/student/Index'
import Submit from '@/components/student/Submit'
import Question from "@/components/student/Question"
import AnswerQuestion from '@/components/student/AnswerQuestion.vue'
import Contest from "@/components/student/Contest"
import Question_contest from "@/components/student/Question_contest"
import AnswerQuestion_contest from '@/components/student/AnswerQuestion_contest.vue'
import Community from "@/components/student/Community"
import ArticleEditor from "@/components/student/ArticleEditor"
import ArticleDetails from "@/components/student/ArticleDetails"


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
      name: 'admin',
      component: ManageUsers
    },
    {
      path: '/admin/user/:id',
      name: 'user',
      component: ManageUsers
    },
    {
      path: '/admin/user/:id/edit',
      name: 'edit-user',
      component: ManageUsers
    },

    {
      path: '/admin/user/:id/delete',
      name: 'delete-user',
      component: ManageUsers
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
      path: '/teacher/community/edit',
      name: 'article-editor_t',
      component: ArticleEditor_t
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
    {
      path: '/student/community/edit',
      name: 'article-editor',
      component: ArticleEditor
    },
    {
      path: '/student/community/:id',
      name: 'article-details',
      component: ArticleDetails
    },
    {
      path: '/teacher/create',
      name: 'create',
      component: CreateExam
    }
    
    
  ]
})
