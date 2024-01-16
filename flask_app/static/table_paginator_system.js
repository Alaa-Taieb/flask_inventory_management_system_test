
class PaginatedTable{
    /**
     * The constructor function creates a table with pagination based on the provided data and desired
     * format.
     * @param table_container_id - The ID of the HTML element that will contain the table.
     * @param fetch_method - The `fetch_method` parameter is a function that is used to fetch data for
     * the table. 
     * @param [data] - An array of objects that contains the data to be displayed in the table.
     * @param [desired_format] - The `desired_format` parameter is an object that specifies the desired
     * format for the table data.
     * @param [page_number=0] - The current page number of the table.
     * @param [rows_per_page=0] - The number of rows to display per page in the table.
     * @param [total_pages=1] - The total number of pages in the table.
     */
    constructor(table_container_id , fetch_method , data = [] , desired_format = {} , page_number = 0 , rows_per_page = 0 , total_pages = 1){
        this.table_container = document.querySelector(`#${table_container_id}`);
        if (!this.table_container){
            console.error(`Search for element with id ${table_container_id} returned null.`);
            console.error(`Table creation failed!`);
        }else{
            this.data = data;
            this.desired_format = desired_format;
            this.page_number = page_number;
            this.rows_per_page = rows_per_page;
            this.total_pages = total_pages;
            this.table = null;
            this.table_head = null;
            this.table_body = null;

            this.pagination_container = null;
            this.fetch_method = fetch_method;


            this.populateTable();
            this.constructPaginator();
        }
    }

    /**
     * The function constructs a table element with a striped style and appends it to a container
     * element.
     */
    constructTable(){
        this.table = document.createElement("table");
        this.table.classList = "table table-striped";
        
        this.table_head = document.createElement("thead");
        this.table_body = document.createElement("tbody");

        this.table.appendChild(this.table_head);
        this.table.appendChild(this.table_body);

        this.table_container.appendChild(this.table);
    }

    /**
     * The `destructTable` function removes the table element and sets the table, table_head, and
     * table_body variables to null.
     */
    destructTable(){
        this.table.remove();
        this.table = null;
        this.table_head = null;
        this.table_body = null;
    }

    /**
     * The function `populateTable` updates the data to display, constructs a table with headers and
     * rows based on the desired format, populates the table body with values from the data list, and
     * constructs a paginator.
     * @param [data] - The `data` parameter is an array of objects that contains the data to be
     * displayed in the table. Each object in the array represents a row in the table, and the
     * properties of the object represent the values in each column of the row.
     */
    populateTable(data = this.data){
        // Update the data to display
        this.setData(data);

        // If the table exists then deconstruct it
        if (this.table){
            this.destructTable();
        }

        // Construct the table
        this.constructTable();    
        
        // Initialize the table headers from the 'desired_format' attribute
        Object.values(this.desired_format).forEach(value => {
            let table_head_column = document.createElement('th');
            table_head_column.innerText = value;
            this.table_head.appendChild(table_head_column);
        });

        // Populate the table body with values from the 'data' list
        this.data.forEach((item) => {
            let new_row = document.createElement('tr');
            this.table_body.appendChild(new_row);
            Object.values(this.desired_format).forEach(value => {
                let new_col = document.createElement('td');
                new_col.innerText = item[value];
                new_row.appendChild(new_col);
            })
        });

        // Construct the paginator.
        this.constructPaginator();
    }

    /**
     * The function "deconstructPaginator" removes the pagination container and sets it to null.
     */
    deconstructPaginator(){
        this.pagination_container.remove();
        this.pagination_container = null;
    }

    
    /**
     * The constructPaginator function creates a pagination container with numbered buttons and
     * previous/next buttons for navigating through pages.
     */
    constructPaginator(){
        // If a paginator exists delete it
        if (this.pagination_container)
            this.deconstructPaginator();

        // Increment page_number by 1 so we eliminate the value 0
        this.page_number++;

        // Create the pagination container and append it to the table_container
        this.pagination_container = document.createElement("ul");
        this.pagination_container.classList = "pagination";
        this.table_container.appendChild(this.pagination_container);

        // Create the 'previous' and 'next' buttons
        const previous_container = document.createElement("li");
        const previous_button = document.createElement("button");
        const next_container = document.createElement("li");
        const next_button = document.createElement("button");

        // Set up the structure of the 'previous' button
        // If we are on the first page we disable the 'previous' button
        previous_container.classList = `page-item ${this.page_number == 1 ? 'disabled' : ''}`;
        previous_button.classList = "page-link";
        previous_button.innerText = "Previous";
        // Add a JavaScript EventListener to the 'previous' button with fetch method associated with this object as a callback function.
        previous_button.addEventListener("click" , () => this.fetch_method(this.page_number - 2 , this.rows_per_page , this.desired_format));
        // Append this button before everything so it stays to on the left.
        previous_container.appendChild(previous_button);
        this.pagination_container.appendChild(previous_container);

        // Create the numbered buttons between the 'previous' and 'next' button
        for( let i = 1 ; i < this.total_pages + 1 ; i++){
            // Create the button_container and it's button | button_container is the 'li' item
            let item = document.createElement("li");
            let button = document.createElement("button");
            // If we are on the iteration number that matches the current selected page number then make the button active.
            item.classList = `page-item ${this.page_number == i ? 'active' : ''}`;

            button.classList = "page-link";
            button.innerText = i;
            // Add a JavaScript EventListener to the button created on this iteration with the fetch method associated with this object as a callback function.
            button.addEventListener("click" , () => this.fetch_method(i - 1 , this.rows_per_page , this.desired_format));

            item.appendChild(button);
            this.pagination_container.appendChild(item);
        }
        // Set up the structure of the 'next' button
        // If we are on the last page we disable the 'next' button
        next_container.classList = `page-item ${this.page_number == this.total_pages ? 'disabled' : ''}`;
        next_button.classList = "page-link";
        next_button.innerText = "Next";
        // Add a JavaScript EventListener to the 'next' button with fetch method associated with this object as a callback function.
        next_button.addEventListener("click" ,() => this.fetch_method(this.page_number , this.rows_per_page , this.desired_format));
        // Append this button after everything so it stays to on the right.
        next_container.appendChild(next_button);
        this.pagination_container.appendChild(next_container);
    }


    /**
     * The function sets the value of the "data" property in the current object.
     * @param data - The "data" parameter is the value that you want to set for the "data" property of
     * the object.
     */
    setData(data){
        this.data = data;
    }

    /**
     * The function sets the desired format for a variable.
     * @param desired_format - The desired format is a variable that represents the format that you
     * want to set for something. It could be a specific file format, data format, or any other format
     * that you want to specify.
     */
    setDesiredFormat(desired_format){
        this.desired_format = desired_format;
    }

    /**
     * The function sets the page number for a specific object.
     * @param page_number - The parameter "page_number" is a variable that represents the page number
     * that you want to set.
     */
    setPageNumber(page_number){
        this.page_number = page_number;
    }

    /**
     * The function sets the number of rows per page.
     * @param rows_per_page - The parameter "rows_per_page" is a variable that represents the number of
     * rows to be displayed per page in a table or grid.
     */
    setRowsPerPage(rows_per_page){
        this.rows_per_page = rows_per_page;
    }

    /**
     * The function sets the total number of pages for a document.
     * @param total_pages - The total number of pages in a document or book.
     */
    setTotalPages(total_pages){
        this.total_pages = total_pages;
    }
}


export {PaginatedTable}




