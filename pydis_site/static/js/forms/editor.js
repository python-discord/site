const QUESTION_TYPES = {
    dropdown: {
        hasOptions: true
    },
    checkbox: {
        hasOptions: true
    },
    text: {
        hasOptions: false
    },
    section: {
        hasOptions: false
    },
    radio: {
        hasOptions: true
    }
}

function swap(arr, from, to) {
    arr.splice(from, 1, arr.splice(to, 1, arr[from])[0]);
}

Vue.component('question', {
    props: ["question", "questions"],
    template: `
<div class="question">
    <h2>{{ question.title }}</h2>


    <button class="small dangerous button" v-on:click="questions.splice(questions.indexOf(question), 1)">Delete question</button>
    <button class="small secondary button" v-on:click="moveUp(questions.indexOf(question))"><i class="fas fa-arrow-up"></i></button>
    <button class="small secondary button" v-on:click="moveDown(questions.indexOf(question))"><i class="fas fa-arrow-down"></i></button>

    <br/><br/>

    <strong>Question title: <input type="text" class="text" v-model="question.title" placeholder="title"/></strong>
    <br/>
    <strong>Unique question identifier: <input v-on:keyup="validateID" type="text" class="text" v-model="question.id" placeholder="ID"/></strong>

    <br/>

    <strong>Type:
        <select v-model="question.type">
            <option v-for="(_, type) in questionTypes" :key="type" :value="type">{{ type }}</option>
        </select>
    </strong>

    <br/>
    <br/>

    <li v-for="option in question.options" v-if="questionTypes[question.type].hasOptions" :key="option">
        {{ option }}
        <span class="button small icon dangerous" v-on:click="question.options.splice(question.options.indexOf(option), 1)">&times;</span>
    </li>
    <br/>

    <input type="text" v-on:keyup.enter="pushInput" class="text" v-if="questionTypes[question.type].hasOptions" v-model="optionInput" placeholder="Option"/>
    
    <button class="small primary button" v-if="questionTypes[question.type].hasOptions" v-on:click="pushInput" style="margin-left: 10px;">Add option</button>
</div>`,
    data: function() {
        return{
            optionInput: null,
            questionTypes: QUESTION_TYPES,
        }
    },
    methods: {
        pushInput: function () {
            this.question.options.push(this.optionInput);
            this.optionInput = "";
        },
        validateID: function () {
            this.question.id = this.question.id.replace(/[- ]/g, '_');
            this.question.id = this.question.id.replace(/[^a-zA-Z0-9_]/g, '');
        },
        moveUp: function (index) {
            if (index != 0) {
                swap(this.questions, index, index - 1);
            }
        },
        moveDown: function (index) {
            if (index != this.questions.length - 1) {
                swap(this.questions, index, index + 1);
            }
        }
    }
  })

var app = new Vue({
    el: '#app',
    delimiters: ["<%","%>"], // Change delimiters to something other than {{ }} for Django templates
    data: {
      questions: JSON.parse(document.getElementById("questions").textContent),
      inputs: {}
    },
    methods: {
        addNewQuestion: function () {
            this.questions.push({
                "id": "question_id",
                "title": "Question title",
                "type": "checkbox",
                "options": []
            })
        },
        saveQuestions: function () {
            fetch(`/forms/questions/${window.formID}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": window.csrftoken
                },
                body: JSON.stringify({
                    questions: this.questions,
                })
            }).then(resp => resp.json()).then(body => {
                if (body.status != "success") {
                    alert(body.message);
                } else {
                    location.reload();
                }
            })
        }
    }
  })