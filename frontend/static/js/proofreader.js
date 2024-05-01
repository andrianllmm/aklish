function generateSuggestions(lang, suggestions, textInput, textMarks, mistakeCount) {
    if (textInput.value.trim().length > 0) {
        suggestions.innerHTML = "";

        let checkNum = 0;
        fetch(`/proofreader/api/?text=${textInput.value}&lang=${lang.value}`)
        .then(response => response.json())
        .then(data => {
            data.checks.forEach(check => {
                checkNum++;
                if (!check.valid) {
                    let wordItem = document.createElement("li");
                    wordItem.classList.add("list-group-item");
                    let head = document.createElement("div");
                    head.classList.add("d-flex", "mb-2");
                    wordItem.appendChild(head);
                    let body = document.createElement("div");
                    body.classList.add("d-flex", "mb-2");
                    wordItem.appendChild(body);

                    let word = document.createElement("u");
                    word.innerHTML = check.token;
                    word.classList.add("flex-grow-1");
                    word.style.textDecorationColor = "red";
                    head.appendChild(word);
                    
                    let replaceSelect = document.createElement("select");
                    replaceSelect.classList.add("form-select", "form-select-sm", "me-auto");
                    replaceSelect.style.width = "150px";
    
                    let replaceOption = document.createElement("option");
                    replaceOption.id = "replace";
                    replaceOption.value = "replace";
                    replaceOption.innerHTML = "Replace";
                    replaceSelect.appendChild(replaceOption);
        
                    let replaceAllOption = document.createElement("option");
                    replaceAllOption.id = "replace-all";
                    replaceAllOption.value = "replace-all";
                    replaceAllOption.innerHTML = "Replace all";
                    replaceSelect.appendChild(replaceAllOption);

                    body.appendChild(replaceSelect);

                    let suggestionGroup = document.createElement("div");
                    let suggestionNum = 0;
                    for (let suggestion of check.suggestions) {
                        suggestionNum++;
                        let suggestionItem = document.createElement("button");
                        suggestionItem.innerHTML = suggestion;
                        suggestionItem.classList.add("suggestion", "btn", "btn-sm", "btn-secondary", "me-1");
                        suggestionItem.setAttribute("data-changefrom", check.token);
                        suggestionItem.setAttribute("data-changeto", suggestion);
            
                        suggestionItem.onclick = (event) => {
                            let changefrom = event.target.getAttribute("data-changefrom");
                            let changeto = event.target.getAttribute("data-changeto");
                            
                            if (document.querySelector("#replace").selected === true) {
                                textInput.value = textInput.value.replace(new RegExp(`\\b${escapeRegExp(changefrom)}\\b`), changeto);
                            } else if (document.querySelector("#replace-all").selected === true) {
                                textInput.value = textInput.value.replace(new RegExp(`\\b${escapeRegExp(changefrom)}\\b`, "g"), changeto);
                            }
                
                            generateSuggestions(lang, suggestions, textInput, textMarks, mistakeCount);
                            generateMarks(lang, textMarks, textInput, mistakeCount);
                        }

                        suggestionGroup.appendChild(suggestionItem);
                    }
                    body.appendChild(suggestionGroup);
            
                    suggestions.appendChild(wordItem);
                }
            });
            if (suggestions.children.length <= 0) {
                suggestions.innerHTML = "No mistakes found.";
            }
        })
    } else {
        suggestions.innerHTML = "Start typing to get suggestions.";
    }
}

function generateMarks(lang, textMarks, textInput, mistakeCount) {
    if (textInput.value.trim().length > 0) {
        textMarks.innerHTML = textInput.value;

        let mistakes = 0;
        fetch(`/proofreader/api/?text=${textInput.value}&lang=${lang.value}`)
        .then(response => response.json())
        .then(data => {
            data.checks.forEach(check => {
                if (!check.valid) {
                    mistakes++;
                    textMarks.innerHTML = textMarks.innerHTML
                    .replace(new RegExp(`\\b${escapeRegExp(check.token)}\\b(?!</u>)`), `<u class="mispelled">${check.token}</u>`);
                }
            });
            mistakeCount.innerHTML = mistakes;
        })
    } else {
        textMarks.innerHTML = "";
    }
}

function countWords(string) {
    let words = string.split(/\s+/);
    words = words.filter((entry) => /\S/.test(entry));
    return (words.length);
}

function calCorrectness(wordCount, mistakeCount) {
    if (parseInt(wordCount.innerHTML) === 0) {
        return ("%");
    } else if (parseInt(mistakeCount.innerHTML) === 0) {
        return ("100%");
    } else {
        let correctness = Math.round(100 * (1 - (parseInt(mistakeCount.innerHTML) / parseInt(wordCount.innerHTML)))) + "%";
        return (correctness);
    }
}

function escapeRegExp(string) {
    return string.replace(/[-[\]{}()*+?.,\\^$|]/g, "\\$&");
}

const containsWhitespace = (string) => /\s/.test(string);

document.addEventListener("DOMContentLoaded", () => {
    let lang = document.querySelector("#lang");
    let textInput = document.querySelector("#proofreader-text-input");
    let textMarks = document.querySelector("#proofreader-text-marks");
    let suggestions = document.querySelector("#proofreader-suggestions");
    let showSuggestions = document.querySelector("#show-suggestions");
    let hideSuggestions = document.querySelector("#hide-suggestions");
    let wordCount = document.querySelector("#word-count");
    let mistakeCount = document.querySelector("#mistake-count");
    let correctness = document.querySelector("#correctness");

    wordCount.innerHTML = 0;
    mistakeCount.innerHTML = 0;
    correctness.innerHTML = "%"

    textInput.onkeyup = () => {
        suggestions.innerHTML = "Writing...";
        generateMarks(lang, textMarks, textInput, mistakeCount);
        wordCount.innerHTML = countWords(textInput.value);
        if (parseInt(wordCount.innerHTML) === 0) {
            mistakeCount.innerHTML = 0;
        }
        correctness.innerHTML = "%";
    }

    showSuggestions.onclick = (event) => {
        event.preventDefault();
        generateSuggestions(lang, suggestions, textInput, textMarks, mistakeCount);
        correctness.innerHTML = calCorrectness(wordCount, mistakeCount);
        document.querySelector("#proofreader-suggestions-col").removeAttribute("hidden");
        hideSuggestions.removeAttribute("hidden");
    }

    hideSuggestions.onclick = (event) => {
        event.preventDefault();
        document.querySelector("#proofreader-suggestions-col").setAttribute("hidden", true);
        hideSuggestions.setAttribute("hidden", true);
    }

    lang.onchange = () => {
        generateMarks(lang, textMarks, textInput, mistakeCount);
        generateSuggestions(lang, suggestions, textInput, textMarks, mistakeCount);
        correctness.innerHTML = calCorrectness(wordCount, mistakeCount);
    }
})