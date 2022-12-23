MathJax = {
    tex: {
        inlineMath: [['\\$', '\\$']],
        displayMath: [['\\$\\$', '\\$\\$']]
    },
    svg: {
        fontCache: 'global'
    },
    skipStartupTypeset: true
};
  
const question_type = {
    "Vector Projection": "vector_proj"
}
$( function() {
    
    qna_template = document.querySelector("#qna-template");
    $('button#gen-q-btn').on('click', function(e) {
        selection = document.querySelector("#select-question-type > .dropdown-toggle").innerHTML;
        if (!(selection in question_type)) {
            alert("Please choose a question type.");
            return;
        }
        q_type = question_type[selection];
        // q_type = "vector_proj";
        e.preventDefault();
        $.get('/generate-question', {"q_type":q_type}, function (data) {
            console.log(data);
            question = document.querySelector("#question");
            question.innerHTML = ""
            question_paragraph = document.createElement('p');
            question_paragraph.innerHTML = data["question"];
            question.appendChild(question_paragraph);
            for (let i = 0; i < data["num_questions"]; i++) {
                const clone = qna_template.content.cloneNode(true);
                clone.querySelector('.part-question-no').innerHTML = '(' + String.fromCharCode(97+i) + ') ';
                clone.querySelector('.part-question').innerHTML = data["q" + (i+1)];
                clone.querySelector('.part-answer').innerHTML = data["a" + (i+1)];
                question.appendChild(clone);
            }

            MathJax.typesetPromise(); // you can play with promises later
            
            // add event listeners to collapsibles
            parts = document.querySelectorAll(".part");
            console.log(parts);
            parts.forEach(function (part) {
                part.querySelector(".part-question-bar").addEventListener("click", function(e) {
                    part.classList.toggle("active");
                    console.log("ey");
                });
            });
        
        });
    });

    dropdown = document.querySelectorAll(".dropdown");
    dropdown.forEach( function(dd) {
        btn = dd.querySelector(".dropdown-toggle");
        items = dd.querySelectorAll(".dropdown-item");
        items.forEach( function(item) {
            item.addEventListener("click", function(e) {
                btn.innerHTML = item.innerHTML;
                btn.classList.add("btn-primary");
                btn.classList.remove("btn-outline-primary");
            })
        });
    });

    
});