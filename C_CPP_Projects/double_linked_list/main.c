#include <stdio.h>
#include <stdlib.h>

/* STRUCT definitions */
struct node_t {
    int data;
    struct node_t *next;
    struct node_t *prev;
};

struct doubly_linked_list_t {
    struct node_t *head;
    struct node_t *tail;
};

/* FUNCTIONS Definitions */

struct doubly_linked_list_t* dll_create() {
    struct doubly_linked_list_t* new_list = (struct doubly_linked_list_t*)malloc(sizeof(struct doubly_linked_list_t));
    if (new_list) {
        new_list->head = NULL;
        new_list->tail = NULL;
    }
    return new_list;
}

int dll_push_back(struct doubly_linked_list_t* dll, int value) {
    if (!dll)
        return 1;

    struct node_t* new_node = (struct node_t*)malloc(sizeof(struct node_t));
    if (!new_node)
        return 2;

    new_node->data = value;
    new_node->next = NULL;

    if (dll->tail) {
        new_node->prev = dll->tail;
        dll->tail->next = new_node;
        dll->tail = new_node;
    } else {
        new_node->prev = NULL;
        dll->head = new_node;
        dll->tail = new_node;
    }

    return 0;
}

int dll_push_front(struct doubly_linked_list_t* dll, int value) {
    if (!dll)
        return 1;

    struct node_t* new_node = (struct node_t*)malloc(sizeof(struct node_t));
    if (!new_node)
        return 2;

    new_node->data = value;
    new_node->prev = NULL;

    if (dll->head) {
        new_node->next = dll->head;
        dll->head->prev = new_node;
        dll->head = new_node;
    } else {
        new_node->next = NULL;
        dll->head = new_node;
        dll->tail = new_node;
    }

    return 0;
}

int dll_pop_front(struct doubly_linked_list_t* dll, int *err_code) {
    if (!dll || !dll->head) {
        if (err_code)
            *err_code = 1;  // 1 oznacza błędne dane wejściowe
        return -1;
    } else if (err_code)
        *err_code = 0;

    int data = dll->head->data;
    if (dll->head == dll->tail) {
        dll->head = NULL;
        dll->tail = NULL;
    } else {
        dll->head = dll->head->next;
        dll->head->prev = NULL;
    }

    return data;
}

int dll_pop_back(struct doubly_linked_list_t* dll, int *err_code) {
    if (!dll || !dll->tail) {
        if (err_code)
            *err_code = 1;  // 1 oznacza błędne dane wejściowe
        return -1;
    } else if (err_code)
        *err_code = 0;

    int data = dll->tail->data;
    if (dll->head == dll->tail) {
        dll->head = NULL;
        dll->tail = NULL;
    } else {
        dll->tail = dll->tail->prev;
        dll->tail->next = NULL;
    }

    return data;
}

int dll_front(const struct doubly_linked_list_t* dll, int *err_code) {
    if (!dll || !dll->head) {
        if (err_code)
            *err_code = 1;
        return -1;
    } else if (err_code)
        *err_code = 0;


    return dll->head->data;
}

int dll_back(const struct doubly_linked_list_t* dll, int *err_code) {
    if (!dll || !dll->tail) {
        if (err_code)
            *err_code = -1;  // -1 oznacza błąd
        return -1;
    } else if (err_code)
        *err_code = 0;

    return dll->tail->data;
}

struct node_t* dll_begin(struct doubly_linked_list_t* dll) {
    if (!dll)
        return NULL;

    return dll->head;
}

struct node_t* dll_end(struct doubly_linked_list_t* dll) {
    if (!dll)
        return NULL;

    return dll->tail;
}

int dll_size(const struct doubly_linked_list_t* dll) {
    if (!dll)
        return -1;

    int count = 0;
    struct node_t* current = dll->head;
    while (current != NULL) {
        count++;
        current = current->next;
    }
    return count;
}

int dll_is_empty(const struct doubly_linked_list_t* dll) {
    if (!dll)
        return -1;
    return (dll->head == NULL) ? 1 : 0;
}

int dll_at(const struct doubly_linked_list_t* dll, unsigned int index, int *err_code) {
    int size = dll_size(dll);
    if (size == -1 || index > size)
    {
        if (err_code)
            *err_code = 1;
        return -1;
    }

    struct node_t* current = dll->head;
    int count = 0;

    while (current != NULL && count < index) {
        current = current->next;
        count++;
    }

    if (err_code)
        *err_code = 0;

    return current->data;
}

int dll_insert(struct doubly_linked_list_t* dll, unsigned int index, int value) {
    if (!dll || index < 0 || index > dll_size(dll))
        return 1;

    if (index == 0)
        return dll_push_front(dll, value);
    else if (index == dll_size(dll))
        return dll_push_back(dll, value);

    struct node_t* current = dll->head;
    int count = 0;

    while (current != NULL && count < index) {
        current = current->next;
        count++;
    }
    if (count != index) {
        return 1;
    }

    struct node_t* new_node = (struct node_t*)malloc(sizeof(struct node_t));
    if (!new_node)
        return 2;

    new_node->data = value;
    new_node->prev = current->prev;
    new_node->next = current;

    if (current->prev)
        current->prev->next = new_node;
    else
        dll->head = new_node;

    current->prev = new_node;

    return 0;
}

int dll_remove(struct doubly_linked_list_t* dll, unsigned int index, int *err_code) {
    if (!dll || index < 0 || index > dll_size(dll)) {
        if (err_code)
            *err_code = 1;
        return -1;
    }

    if (index == 0)
        return dll_pop_front(dll, err_code);
    else if (index == dll_size(dll))
        return dll_pop_back(dll, err_code);

    struct node_t* current = dll->head;
    int count = 0;

    while (current != NULL && count < index) {
        current = current->next;
        count++;
    }

    if (current->prev)
        current->prev->next = current->next;
    else
        dll->head = current->next;

    if (current->next)
        current->next->prev = current->prev;
    else
        dll->tail = current->prev;

    if (err_code)
        *err_code = 0;

    int data = current->data;
    free(current);
    return data;
}

void dll_clear(struct doubly_linked_list_t* dll) {
    if (!dll)
        return;

    struct node_t* current = dll->head;
    while (current != NULL) {
        struct node_t* next = current->next;
        free(current);
        current = next;
    }

    dll->head = NULL;
    dll->tail = NULL;
}

void dll_display(const struct doubly_linked_list_t* dll) {
    if (!dll)
        return;

    struct node_t* current = dll->head;
    while (current != NULL) {
        printf("%d ", current->data);
        current = current->next;
    }

    printf("\n");
}

void dll_display_reverse(const struct doubly_linked_list_t* dll) {
    if (!dll)
        return;

    struct node_t* current = dll->tail;
    while (current != NULL) {
        printf("%d ", current->data);
        current = current->prev;
    }

    printf("\n");
}


int main() {
    struct doubly_linked_list_t* dll = dll_create();
    if (!dll) {
        printf("Failed to allocate memory\n");
        return 8;
    }

    int choice;
    int data;
    int value, index, err_code;
    do {
        printf("\nMenu:\n");
        printf("0 - Exit\n");
        printf("1 - Add element to the end\n");
        printf("2 - Remove last element\n");
        printf("3 - Add element to the beginning\n");
        printf("4 - Remove first element\n");
        printf("5 - Add element at a specific index\n");
        printf("6 - Remove element at a specific index\n");
        printf("7 - Display last element\n");
        printf("8 - Display first element\n");
        printf("9 - Check if the list is empty\n");
        printf("10 - Display the number of elements\n");
        printf("11 - Clear the list\n");
        printf("12 - Display element at a specific index\n");
        printf("13 - Display all elements\n");
        printf("14 - Display all elements in reverse\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 0:
                break;
            case 1:
                printf("Enter value to add to the end: ");
                scanf("%d", &value);
                if (dll_push_back(dll, value) == 2) {
                    printf("Failed to allocate memory\n");
                    return 8;
                }
                break;
            case 2:
                data = dll_pop_back(dll, &err_code);
                if (err_code == 0)
                {
                    printf("Removed element: %d\n", data);
                }
                else {
                    printf("List is empty\n");
                }
                break;
            case 3:
                printf("Enter value to add to the beginning: ");
                scanf("%d", &value);
                if (dll_push_front(dll, value) == 2) {
                    printf("Failed to allocate memory\n");
                    return 8;
                }
                break;
            case 4:
                data = dll_pop_front(dll, &err_code);
                if (err_code == 0) {
                    printf("Removed element: %d\n", data);
                } else {
                    printf("List is empty\n");
                }
                break;
            case 5:
                printf("Enter value to add: ");
                scanf("%d", &value);
                printf("Enter index to add at: ");
                scanf("%d", &index);
                data = dll_insert(dll, index, value);
                if (data == 2) {
                    printf("Failed to allocate memory\n");
                    return 8;
                } else if (data == 1) {
                    printf("Index out of range\n");
                }
                break;
            case 6:
                if (dll_is_empty(dll) == 1)
                {
                    printf("List is empty\n");
                    break;
                }
                printf("Enter index to remove: ");
                scanf("%d", &index);
                data = dll_remove(dll, index, &err_code);
                if (err_code == 0) {
                    printf("Removed element: %d\n", data);
                } else if (err_code == 1) {
                    printf("Index out of range\n");
                }
                break;
            case 7:
                data = dll_back(dll, &err_code);
                if (err_code == 0) {
                    printf("Last element: %d\n", data);
                } else {
                    printf("List is empty\n");
                }
                break;
            case 8:
                data = dll_front(dll, &err_code);
                if (err_code == 0) {
                    printf("First element: %d\n", data);
                } else {
                    printf("List is empty\n");
                }
                break;
            case 9:
                printf("Is the list empty: %d\n", dll_is_empty(dll));
                break;
            case 10:
                printf("Number of elements: %d\n", dll_size(dll));
                break;
            case 11:
                dll_clear(dll);
                break;
            case 12:
                if (dll_is_empty(dll) == 1)
                {
                    printf("List is empty\n");
                    break;
                }
                printf("Enter index to display: ");
                scanf("%d", &index);
                data = dll_at(dll, index, &err_code);
                if (err_code == 0) {
                    printf("Element at index %d: %d\n", index, data);
                } else {
                    printf("Index out of range\n");
                }
                break;
            case 13:
                dll_display(dll);
                break;
            case 14:
                dll_display_reverse(dll);
                break;
            default:
                printf("Incorrect input data\n");
        }
    } while (choice != 0);
    
    dll_clear(dll);
    free(dll);

    return 0;
}
