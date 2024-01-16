import { show_messages_v2 } from './alert_message.js';
import { PaginatedTable } from './table_paginator_system.js';

const add_product_form = document.querySelector("#add_product_form");
const products_table_container_id = "products_list_container";


/* These lines of code are selecting specific elements from the HTML document using their respective
IDs. */
const check_reference_button = document.querySelector("#check_reference_button");
const check_reference_icon = document.querySelector("#check_reference_button > img");
const check_reference_text = document.querySelector("#check_reference_button > span");
const submit_add_product_button = document.querySelector("#submit_add_product_button");

/* These lines of code are declaring constants that are used in the JavaScript code. */
const REFERENCE_CHECK_URL = "/products/check_reference";
const CREATE_PRODUCT_URL = "/products/create";
const GET_PRODUCTS_PAGINATED_URL = "/products/get_all_paginated";
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

let products_table = new PaginatedTable(products_table_container_id , get_products_paginated);

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
    // Set form Validity to true (Using the appropriate method)
    set_form_validity()
    if (ref_validity){
        // Change the check button to be success class and check_mark icon
        check_reference_button.classList.remove(DANGER_BUTTON_CLASS);
        check_reference_button.classList.add(SUCCESS_BUTTON_CLASS);
        check_reference_button.disabled = true;
        check_reference_icon.src = CHECK_MARK_WHITE_URL;
        
        check_reference_text.innerHTML = check_reference_text.innerHTML.replace("Check" , "Valid");
        
    }else{
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

/* The code `add_product_form.onsubmit` is assigning an event handler function to the `onsubmit` event
of the `add_product_form` element. */
add_product_form.onsubmit = (e) => {
    e.preventDefault();
    let form = new FormData(add_product_form);
    fetch(CREATE_PRODUCT_URL , {method:'POST' , body: form })
    .then(res => res.json())
    .then(data => {
        if (data.category == 'success'){
            // Call function to handle Getting products from data base and populating the appropriate rows
            get_products_paginated();
        }
        show_messages_v2(data , 10);
        add_product_form.reset()
    })
    .catch();
}

/**
 * The function `get_products_paginated` fetches paginated product data from a specified URL and
 * populates a table with the desired format.
 * @param [page_number=0] - The page number parameter is used to specify which page of results you want
 * to retrieve. By default, it is set to 0, which means the first page.
 * @param [rows_per_page=7] - The "rows_per_page" parameter determines the number of rows or items to
 * be displayed per page in the paginated results.
 * @param [desired_results_format] - The desired_results_format parameter is an object that specifies
 * the format in which you want the results to be displayed. It has the following properties:
 */
function get_products_paginated(page_number = 0 , rows_per_page = 7 , desired_results_format = {'id': "ID" , 'name': "Name" , 'reference': "Ref." , 'created_at': "Created_at" , 'updated_at': "Updated_at"}){
    let data_request_object = {
        desired_results_format: desired_results_format,
        page_number: page_number,
        rows_per_page: rows_per_page
    }

    fetch(GET_PRODUCTS_PAGINATED_URL , {method:'POST' , body: JSON.stringify(data_request_object)})
    .then(res => res.json())
    .then(data => {
        console.log(data)
        products_table.setDesiredFormat(desired_results_format);
        products_table.setPageNumber(page_number);
        products_table.setRowsPerPage(rows_per_page);
        products_table.setTotalPages(data.number_of_pages);
        products_table.populateTable(data.products);
        // populate_table("products_list_container" , data.products , desired_results_format , page_number , rows_per_page , data.number_of_pages);
    })
}


// Call once on load
get_products_paginated()

window.check_reference = check_reference;
window.switch_reference_status = switch_reference_status;