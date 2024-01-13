import { show_messages_v2 } from './alert_message.js';

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
        show_messages_v2(data.messages_object , 5);
    })
    .catch()
}


window.check_reference = check_reference;
window.switch_reference_status = switch_reference_status;