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
    "Vector Projection": "vector_proj",
    "System of Equations": "system_of_eq"
}
$( function() {

    document.documentElement.setAttribute("data-theme", "dark");

    const tag_sections = document.querySelectorAll(".tags");
    tag_sections.forEach(function (tag_section) {
        var tags = tag_section.innerHTML.split(",");
        tag_section.innerHTML = tags.map((tag) => `<a class='tag' href='#'>${tag}</a>`).join("")
    })

    const pathname = window.location.pathname;
    console.log(pathname);
    if (pathname != "/") {
        const sections = pathname.split('/').slice(1);
        console.log(sections)
        var path = "";
        const tags = [];
        for (var i = 0; i < sections.length; i++) {
            path += "/" + sections[i];
            tags.push(`<a class="section" href="${path}">${sections[i]}</a>`);
        }
        document.querySelector('.pathname').innerHTML = "<a class='section' href='/'>home</a>/" + tags.join("/");
    }

    qna_template = document.querySelector("#qna-template");
    $('button#gen-q-btn').on('click', function(e) {
        selection = document.querySelector("#select-question-type > .dropdown-toggle").innerHTML;
        if (!(selection in question_type)) {
            alert_elm = document.querySelector("#question-alert");
            alert_elm.classList.add("alert-danger"); alert_elm.classList.remove("alert-success");
            alert_elm.querySelector("div").innerHTML = "Please choose a valid question type!";
            alert_elm.querySelector("button").addEventListener("click", function() {alert_elm.classList.remove("alert-fade");})
            console.log(alert_elm);
            alert_elm.classList.add("alert-fade");
            setTimeout(function() {alert_elm.classList.remove("alert-fade");}, 3000);
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
                    ans = part.querySelector(".part-answer-wrapper")
                    if (ans.style.maxHeight){
                        ans.style.maxHeight = null;
                    } else {
                        ans.style.maxHeight = ans.scrollHeight + "px";
                    }
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