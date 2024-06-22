<template>
    <div class="answer-page">
      <h2>Answer Problem #{{ selectedProblem.id }}</h2>
      <div class="problem-content">
        <div class="problem-description">
          <strong>Title:</strong> {{ selectedProblem.title }} <br>
          <strong>Difficulty:</strong> {{ selectedProblem.difficulty }} <br>
          <strong>Keywords:</strong> {{ selectedProblem.keywords.join(', ') }}
        </div>
        <textarea v-model="sqlAnswer" placeholder="Enter your SQL code here..."></textarea>
        <button @click="submitAnswer">Submit</button>
      </div>
    </div>
  </template>
     
  