const add_product_form = document.querySelector("#add_product_form");

/* These lines of code are selecting specific elements from the HTML document using their respective
IDs. */
const check_reference_button = document.querySelector("#check_reference_button");
const check_reference_icon = document.querySelector("#check_reference_button > img");
const check_reference_text = document.querySelector("#check_reference_button > span");
const submit_add_product_button = document.querySelector("#submit_add_product_button");
const messages_container = document.querySelector("#messages_container");

/* These lines of code are declaring constants that are used in the JavaScript code. */
const REFERENCE_CHECK_URL = "/products/check_reference";
const CHECK_MARK_WHITE_URL = `http://${sessionStorage.getItem('host')}/static/assets/icons/check_mark_white.png`;
const CLOSE_WHITE_URL = `http://${sessionStorage.getItem('host')}/static/assets/icons/close_white.png`;
const SUCCESS_BUTTON_CLASS = "btn-success";
const DANGER_BUTTON_CLASS = "btn-danger";

/* These lines of code are declaring and initializing variables that are used to track the validity of
different form fields. */
let form_validity = false;
let name_validity = true;
let price_validity = true;
let ref_validity = false;

/**
 * The function `switch_reference_status` updates the validity status of a reference and modifies the
 * appearance of a check button accordingly.
 * @param new_validity_status - The new validity status of the reference. It can be either true or
 * false.
 * @returns nothing (undefined).
 */
function switch_reference_status(new_validity_status){
    if (ref_validity == new_validity_status)
        return

    ref_validity = new_validity_status;
    if (ref_validity){
        // Set form Validity to true (Using the appropriate method)
        set_form_validity()
        // Change the check button to be success class and check_mark icon
        check_reference_button.classList.remove(DANGER_BUTTON_CLASS);
        check_reference_button.classList.add(SUCCESS_BUTTON_CLASS);
        check_reference_button.disabled = true;
        check_reference_icon.src = CHECK_MARK_WHITE_URL;
        
        check_reference_text.innerHTML = check_reference_text.innerHTML.replace("Check" , "Valid");
        
    }else{
        // Set form Validity to true (Using the appropriate method)
        set_form_validity()
        // Change the check button to be success class and check_mark icon
        check_reference_button.classList.remove(SUCCESS_BUTTON_CLASS);
        check_reference_button.classList.add(DANGER_BUTTON_CLASS);
        check_reference_button.disabled = false;
        check_reference_icon.src = CLOSE_WHITE_URL;

        check_reference_text.innerHTML = check_reference_text.innerHTML.replace("Valid" , "Check");
        
    }
}



/**
 * The function sets the validity of a form based on the validity of three input fields and disables a
 * submit button if the form is not valid.
 */
function set_form_validity(){
    form_validity = name_validity && price_validity && ref_validity;
    submit_add_product_button.disabled = !form_validity;
}

/**
 * The function `check_reference()` sends a POST request to a specified URL with a reference value,
 * receives a response containing the validity of the reference and messages, and then calls other
 * functions to handle the response.
 */
function check_reference(){
    const data = new FormData(add_product_form);
    let reference = data.get('reference');
    
    const request_form = new FormData();
    request_form.append('reference' , reference);

    fetch(REFERENCE_CHECK_URL, {method:'POST' , body: request_form})
    .then(res => res.json())
    .then(data => {
        
        switch_reference_status(data.ref_validity);
        show_messages(data.messages_object , 5);
    })
    .catch()
}

/**
 * The function `show_messages` displays error or success messages in a message box with a close button
 * and a timer.
 * @param messages_object - The `messages_object` parameter is an object that contains the messages to
 * be displayed. It has the following properties:
 * @param timeout - The timeout parameter is the duration in milliseconds for which the message box
 * will be displayed before automatically closing.
 */
function show_messages(messages_object , timeout){
    let message_box;
    let unordered_list = document.createElement("ul");
    let button = document.createElement("button");
    let timer = document.createElement("span");
    timer.innerText = 0;
    button.appendChild(timer);
    if (messages_object.category == 'error'){
        let displayed_messages = document.querySelectorAll("#messages_container > .error");
        if (displayed_messages.length == 1) {
            message_box = displayed_messages[0];
            unordered_list = message_box.querySelector("ul");
        }else{
            message_box = document.createElement("div");
            
            message_box.classList = "message_box error d-flex justify-content-between align-items-center alert alert-danger";
            unordered_list.classList = "messages";
            button.classList = "btn btn-danger";
            button.innerHTML += " Close";
            message_box.appendChild(unordered_list);
            message_box.appendChild(button);
            button.addEventListener("click" , () => {
                removeMessage(message_box);
            })
        }
        
        if (displayed_messages.length == 0){
            messages_container.appendChild(message_box);
            message_box.style.translate = "0px 100px";
            let time = 250;
            let in_animation = setInterval(() => {
                
                if (current_time == 0){
                    clearInterval(in_animation);
                }else{
                    message_box.style.translate = `0px ${(current_time / time) * 100}px`;
                    message_box.style.opacity =0.8- (current_time / time);
                    current_time -= 5;
                }
            }, 5, time = time, current_time = time);
        }
    }else if(messages_object.category == 'success'){
        let displayed_messages = document.querySelectorAll("#messages_container > .success");
        if (displayed_messages.length == 1) {
            message_box = displayed_messages[0];
            unordered_list = message_box.querySelector("ul");
            
        }else{
            message_box = document.createElement("div");
            message_box.classList = "message_box success d-flex justify-content-between align-items-center alert alert-success";
            console.log(message_box.classList);
            unordered_list.classList = "messages";
            button.classList = "btn btn-success";
            button.innerHTML += " Close";
            message_box.appendChild(unordered_list);
            message_box.appendChild(button);
            button.addEventListener("click" , () => {
                removeMessage(message_box);
            })
        }
        
        console.log(displayed_messages)
        if (displayed_messages.length == 0){
            messages_container.appendChild(message_box);
            message_box.style.translate = "0px 100px";
            let time = 250;
            let in_animation = setInterval(() => {
                
                if (current_time == 0){
                    clearInterval(in_animation);
                }else{
                    message_box.style.translate = `0px ${(current_time / time) * 100}px`;
                    message_box.style.opacity =0.8- (current_time / time);
                    current_time -= 5;
                }
            }, 5, time = time, current_time = time);
        }
    }
    messages_object.messages.forEach(message => {
        let list_item = document.createElement("li");
        list_item.classList = "message";
        list_item.innerText = message;
        unordered_list.appendChild(list_item);
    });
    let container_height = 20;
    messages_container.querySelectorAll(".message_box").forEach(element =>{
        container_height += element.offsetHeight;
        if (element.classList.contains(messages_object.category)){
            
            let current_time = parseInt(element.querySelector("button").querySelector("span").innerText);
            let new_time = current_time + timeout;
            element.querySelector("button").querySelector("span").innerText = new_time;
            if (!element.querySelector('a')){
                let memory_element = document.createElement("a");
                memory_element.style.display = "None";
                element.appendChild(memory_element);
                let interval = setInterval(() => {
                    
                    console.log(new_time)
                    element.querySelector("button").querySelector("span").innerText-= 1;
                    if (element.querySelector("button").querySelector("span").innerText == 0){
                        clearInterval(interval)
                        element.querySelector("a").remove();
                        removeMessage(element)
                    }
                }, 1000 , element = element);
            }
        }
        
    })
    
    messages_container.style.bottom = `${container_height}px`;

    
}

/**
 * The function `removeMessage` is used to animate the removal of a message box by gradually decreasing
 * its opacity and translating it downwards.
 * @param message_box - The `message_box` parameter is the HTML element that represents the message box
 * that you want to remove.
 */
function removeMessage(message_box){
    let time = 250;
    message_box.style.translate = "0px 0px";
    let out_animation = setInterval(() => {
        
        if (current_time == 0){
            message_box.remove();
            clearInterval(out_animation);
        }else{
            message_box.style.translate = `0px ${100-(current_time / time) * 100}px`;
            message_box.style.opacity = (current_time / time);
            current_time -= 5;
        }
    }, 5, time = time, current_time = time);
}