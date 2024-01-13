

function show_messages_v2(message_object , timeout){
    let message_box_object = get_message_box(message_object.category);
    let new_message_box = false;

    let messages_container = document.querySelector("#messages_container");

    if (!message_box_object){
        message_box_object = create_message_box(message_object.category);
        new_message_box = true;
    }

    message_object.messages.forEach(message => {
        let list_item = document.createElement("li");
        list_item.classList = "message";
        list_item.innerText = message;
        message_box_object.unordered_list.appendChild(list_item);
    });

    
    if (new_message_box){
        messages_container.appendChild(message_box_object.message_box);
        start_entrance_animation(message_box_object.message_box , 250 , 5 , {end_opacity : 0.8});
    }
    manage_message_box_countdown_timer(message_box_object , timeout);
    calculate_height_offset(messages_container , 20);



}

/**
 * The function `create_message_box` creates a message box element with specified type and returns an
 * object containing the created elements.
 * @param type - The "type" parameter is a string that determines the type of message box to create. It
 * can have two possible values: "error" or "success".
 * @returns an object that contains the following properties:
 * message_box      -> div
 * unordered_list   -> ul
 * close_button     -> button
 * time_counter     -> span
 * button_text      -> span
 */
function create_message_box(type){
    // Creating the elements
    let message_box = document.createElement("div");
    let unordered_list = document.createElement("ul");
    let close_button = document.createElement("button");
    let time_counter = document.createElement("span");
    let button_text = document.createElement("span");

    // Setting default values as needed.
    time_counter.innerText = 0;
    button_text.innerText = " Close";

    // Setting up element classes.
    message_box.classList = `message_box ${type} d-flex justify-content-between align-items-center alert alert-${(type == "error" ? "danger" : "success")}`;
    unordered_list.classList = "messages";
    close_button.classList = `btn btn-${(type == "error" ? "danger" : "success")}`;
    time_counter.classList = "button_timer";
    button_text.classList = "button_text";

    
    // Adding even listener to the close button to handle closing and removing the alert message
    close_button.addEventListener("click" , () => remove_message_box(message_box , 250 , 5 , {start_opacity : 0.8}));

    // Creating the element hierarchy needed.
    message_box.appendChild(unordered_list);
    close_button.appendChild(time_counter);
    close_button.appendChild(button_text);
    message_box.appendChild(close_button);

    // creating and returning an object containing all the created elements
    let message_box_object = 
    {
        'message_box': message_box,
        'unordered_list': unordered_list,
        'close_button': close_button,
        'time_counter': time_counter,
        'button_text': button_text
    };

    return message_box_object;

}

/**
 * The function `get_message_box` returns an object containing various elements of a message box based
 * on the given type.
 * @param type - The `type` parameter is a string that specifies the type of message box to retrieve.
 * It is used to select the appropriate message box element from the DOM.
 * @returns an object that contains various elements related to a message box.
 */
function get_message_box(type){
    let message_box = document.querySelector(`#messages_container > .${type}`);
    if (!message_box)
        return false;
    let messages_box_element = 
    {
        'message_box': message_box,
        'unordered_list': message_box.querySelector('ul'),
        'close_button': message_box.querySelector('button'),
        init_button_spans(){
            this.time_counter = this.close_button.querySelector('.button_timer');
            this.button_text = this.close_button.querySelector('.button_text');
            return this;
        },
    }.init_button_spans()
    return messages_box_element;
}

/**
 * The function calculates the height offset of a messages container by summing the heights of all
 * message boxes within it and then sets the bottom position of the container accordingly.
 * @param messages_container - The `messages_container` parameter is the container element that holds
 * all the message boxes. It is a DOM element object.
 * @param container_height - The `container_height` parameter represents the current height of the
 * container element.
 */
function calculate_height_offset(messages_container , container_height){
    messages_container.querySelectorAll(".message_box").forEach(element => {
        container_height += element.offsetHeight;
    });
    messages_container.style.bottom = `${container_height}px`;
}

/**
 * The function manages the countdown timer for a message box by adding time to its lifetime and
 * starting the timer if it's a new message box.
 * @param message_box_object - The `message_box_object` parameter is an object that represents the
 * message box element in the DOM. It should have the following properties:
 * @param timeout - The timeout parameter is the amount of time (in seconds) that you want to add to
 * the countdown timer of the message box.
 * @returns an object with two properties: 'status' and 'code'. The 'status' property describes the
 * result of the function, indicating whether the message box lifetime was extended or not. The 'code'
 * property provides a numerical code to represent the result, with 0 indicating a successful extension
 * of the message box lifetime.
 */
function manage_message_box_countdown_timer(message_box_object,timeout){
    // Adding the timeout to the remaining life time of the message
    message_box_object.time_counter.innerText = parseInt(message_box_object.time_counter.innerText) + timeout;
    
    // We want to only start the countdown timer for newly created message boxes, but those that already have a ticking timer will get an increase in their time.
    // And so we will add a memory element to check if we have already started the countdown timer for this message box.
    // If we find that element that means this is not a new message box and we are only adding time to it's timer
    // If we don't find that element that means that this is a new message box and we need to start it's countdown timer.
    if(message_box_object.message_box.querySelector("a"))
        return {'status': "Extended message_box lifetime." , 'code': 0};

    let memory_element = document.createElement("a");
    memory_element.style.display = "None";

    message_box_object.message_box.appendChild(memory_element);

    let interval = setInterval(() => {
        message_box_object.time_counter.innerText -= 1;
        if (message_box_object.time_counter.innerText == 0){
            clearInterval(interval);
            message_box_object.message_box.querySelector("a").remove();
            remove_message_box(message_box_object.message_box , 250 , 5 , {start_opacity : 0.8});
        }
    }, 1000)

    return {'status': "Started countdown timer for the message_box." , 'code': 1};
}

/**
 * The function "start_entrance_animation" animates the entrance of a message box by gradually fading
 * it in and moving it from bottom to top.
 * @param message_box - The HTML element that represents the message box you want to animate.
 * @param animation_length - The total length of the animation in milliseconds.
 * @param [frame_length=5] - The frame_length parameter determines the duration of each frame in the
 * animation. It is measured in milliseconds.
 * @param [type] - The "type" parameter is an array that specifies the type of entrance animation to be
 * applied to the message box. It can contain one or more values from the following options:
 * @param [message_box_y_offset=100] - The `message_box_y_offset` parameter is used to specify the
 * vertical offset of the message box during the animation. It determines how much the message box will
 * move vertically from its initial position.
 * @param [end_opacity=1] - The end_opacity parameter is the final opacity value that the message box
 * should have at the end of the animation. It is a number between 0 and 1, where 0 represents fully
 * transparent and 1 represents fully opaque.
 */
function start_entrance_animation(message_box , animation_length , frame_length = 5 ,type = ["fade_in", "bottom_top"] , message_box_y_offset = 100 , end_opacity = 1){
    message_box.style.translate = `0px ${message_box_y_offset}px`;

    // We need to keep track of the initial and remaining time inside the setInterval callback function so we can plot the animation over the length we desire
    // The problem is passing a variable by value to this callback function will keep repeating the same initial value for the remaining time because the time subtraction  is happening within the function itself.
    // So we need pass a value by reference and the easiest way to this is to create an array containing the initial time at index 0 and the remaining time at index 1
    let time_values = [animation_length , animation_length];
    let animation = setInterval((time_values) => {
        // If time remaining is less or equal to 0 then stop the animation.
        if (time_values[1] <= 0){
            clearInterval(animation);
        }
        else
        {
            message_box.style.translate = `0px ${(time_values[1] / time_values[0]) * 100}px`;
            message_box.style.opacity = end_opacity - (time_values[1] / time_values[0]);
            time_values[1] -= frame_length;
        }
    } , frame_length , time_values);
}

/**
 * The function `remove_message_box` is a JavaScript function that animates the removal of a message
 * box by fading it out and moving it from top to bottom.
 * @param message_box - The HTML element representing the message box that you want to remove.
 * @param animation_length - The total length of the animation in milliseconds. This determines how
 * long the animation will run for.
 * @param [frame_length=5] - The frame_length parameter determines the duration of each frame in
 * milliseconds. It specifies how often the animation should update.
 * @param [type] - The "type" parameter is an optional parameter that specifies the type of animation
 * to be applied to the message box. It can have two possible values: "fade-out" and "top_bottom".
 * @param [message_box_y_offset=0] - The message_box_y_offset parameter is used to specify the vertical
 * offset of the message box from its original position. It allows you to move the message box up or
 * down on the screen.
 * @param [start_opacity=1] - The start_opacity parameter determines the initial opacity of the message
 * box. It is a value between 0 and 1, where 0 represents completely transparent and 1 represents fully
 * opaque.
 */
function remove_message_box(message_box , animation_length , frame_length = 5 , type = ["fade-out" , "top_bottom"] , message_box_y_offset = 100 , start_opacity = 1){
    message_box.style.translate = `0px 0px`;

    // We need to keep track of the initial and remaining time inside the setInterval callback function so we can plot the animation over the length we desire
    // The problem is passing a variable by value to this callback function will keep repeating the same initial value for the remaining time because the time subtraction  is happening within the function itself.
    // So we need pass a value by reference and the easiest way to this is to create an array containing the initial time at index 0 and the remaining time at index 1
    let time_values = [animation_length , animation_length];
    let animation = setInterval((time_values) => {
        // If time remaining is less or equal to 0 then stop the animation.
        if (time_values[1] <= 0){
            message_box.remove();
            clearInterval(animation);
        }
        else
        {
            message_box.style.translate = `0px ${message_box_y_offset-(time_values[1] / time_values[0]) * 100}px`;
            message_box.style.opacity = (time_values[1] / time_values[0]) * start_opacity;
            time_values[1] -= frame_length;
        }
    } , frame_length , time_values);
}
export {show_messages_v2};