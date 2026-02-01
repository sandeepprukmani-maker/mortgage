<template>
    <div class="overflow-x-auto scroll-sm pb-8 d-flex gap-24">
        <!-- Draggable Columns -->
        <draggable v-model="columns" item-key="status" class="kanban-wrapper d-flex gap-24" :group="'columns'"
            :ghost-class="'ghost'" :drag-class="'dragging'">
            <template #item="{ element: column, index }">
                <div class="w-25 kanban-item radius-12 progress-card">
                    <div class="card p-0 radius-12 overflow-hidden shadow-none">
                        <div class="card-body p-0 pb-24">
                            <!-- Check if the column is not 'new' -->
                            <template v-if="column.status !== 'new'">
                                <div class="d-flex align-items-center gap-2 justify-content-between ps-24 pt-24 pe-24">
                                    <h6 class="text-lg fw-semibold mb-0">{{ column.title }}</h6>
                                    <div class="d-flex align-items-center gap-3 justify-content-between mb-0">
                                        <button type="button" class="text-2xl hover-text-primary add-task-button"
                                            @click="openModal(null, column.status)">
                                            <iconify-icon icon="ph:plus-circle" class="icon"></iconify-icon>
                                        </button>
                                        <div class="dropdown">
                                            <button type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                <iconify-icon icon="entypo:dots-three-vertical"
                                                    class="text-xl"></iconify-icon>
                                            </button>
                                            <ul class="dropdown-menu p-12 border bg-base shadow">
                                                <li>
                                                    <a href="#" class="duplicate-button dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900 d-flex align-items-center gap-2"  @click="duplicateColumn(column)">
                                                        <iconify-icon class="text-xl"
                                                            icon="humbleicons:duplicate"></iconify-icon>
                                                        Duplicate
                                                    </a>
                                                </li>
                                                <li>
                                                    <a href="#" class="delete-button dropdown-item px-16 py-8 rounded text-secondary-light bg-hover-neutral-200 text-hover-neutral-900 d-flex align-items-center gap-2"  @click="deleteColumn(index)">
                                                        <iconify-icon class="text-xl"
                                                            icon="mingcute:delete-2-line"></iconify-icon>
                                                        Delete
                                                    </a>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>

                                <!-- Tasks -->
                                <draggable v-model="column.tasks" :group="'tasks'" item-key="id"
                                    class="connectedSortable ps-24 pt-24 pe-24" :ghost-class="'ghost'"
                                    :drag-class="'dragging'">
                                    <template #item="{ element: task }">
                                        <div :key="task.id" class="kanban-card bg-neutral-50 p-16 radius-8 mb-24">
                                            <div v-if="task.image" class="radius-8 mb-12 max-h-350-px overflow-hidden">
                                                <img :src="task.image" alt="" class="w-100 h-100 object-fit-cover" />
                                            </div>
                                            <h6 class="kanban-title text-lg fw-semibold mb-8">{{ task.title }}</h6>
                                            <p class="kanban-desc text-secondary-light">{{ task.description }}</p>
                                            <button type="button"
                                                class="btn text-primary-600 border rounded border-primary-600 bg-hover-primary-600 text-hover-white d-flex align-items-center gap-2">
                                                <iconify-icon icon="lucide:tag" class="icon"></iconify-icon>
                                                <span class="kanban-tag fw-semibold">{{ task.tag }}</span>
                                            </button>
                                            <div class="mt-12 d-flex align-items-center justify-content-between gap-10">
                                                <div class="d-flex align-items-center gap-10">
                                                    <iconify-icon icon="solar:calendar-outline"
                                                        class="text-primary-light"></iconify-icon>
                                                    <span class="start-date text-secondary-light">{{ task.date }}</span>
                                                </div>
                                                <div class="d-flex align-items-center gap-10">
                                                    <button type="button" class="card-edit-button text-success-600"
                                                        @click="openModal(task)">
                                                        <iconify-icon icon="lucide:edit"
                                                            class="icon text-lg line-height-1"></iconify-icon>
                                                    </button>
                                                    <button type="button" class="card-delete-button text-danger-600"
                                                        @click="deleteTask(task.id)">
                                                        <iconify-icon icon="fluent:delete-24-regular"
                                                            class="icon text-lg line-height-1"></iconify-icon>
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </template>
                                </draggable>
                                <button type="button"
                                    class="d-flex align-items-center gap-2 fw-medium w-100 text-primary-600 justify-content-center text-hover-primary-800 add-task-button"
                                    @click="openModal(column.status)">
                                    <iconify-icon icon="ph:plus-circle" class="icon text-xl"></iconify-icon>
                                    Add Task
                                </button>
                            </template>

                            <!-- Always show Add Task button for 'New' column -->
                            <template v-if="column.status === 'new'">
                                <button type="button"
                                    class="d-flex align-items-center gap-2 fw-medium w-100 text-primary-600 justify-content-center text-hover-primary-800 add-task-button p-14 mt-16"
                                    @click="openModal(null, column.status)">
                                    <iconify-icon icon="ph:plus-circle" class="icon text-xl"></iconify-icon>
                                    Add Task
                                </button>
                            </template>
                        </div>
                    </div>
                </div>
            </template>
        </draggable>
    </div>

    <!-- Add/Edit Task Modal -->
    <div class="modal fade" id="addTaskModal" tabindex="-1" aria-labelledby="addTaskModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h6 class="modal-title text-xl mb-0" id="addTaskModalLabel">
                        {{ isEditing ? 'Edit Task' : 'Add New Task' }}
                    </h6>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="taskForm">
                        <input type="hidden" id="editTaskId" v-model="currentTask.id">
                        <div class="mb-3">
                            <label for="taskTitle"
                                class="form-label fw-semibold text-primary-light text-sm mb-8">Title</label>
                            <input type="text" class="form-control" v-model="currentTask.title"
                                placeholder="Enter Event Title" id="taskTitle" required>
                        </div>
                        <div class="mb-3">
                            <label for="taskTag"
                                class="form-label fw-semibold text-primary-light text-sm mb-8">Tag</label>
                            <input type="text" class="form-control" v-model="currentTask.tag" placeholder="Enter tag"
                                id="taskTag" required>
                        </div>
                        <div class="mb-3">
                            <label for="startDate" class="form-label fw-semibold text-primary-light text-sm mb-8">Start
                                Date</label>
                            <input type="date" class="form-control" v-model="currentTask.date" id="startDate" required>
                        </div>
                        <div class="mb-3">
                            <label for="taskDescription"
                                class="form-label fw-semibold text-primary-light text-sm mb-8">Description</label>
                            <textarea class="form-control" v-model="currentTask.description" id="taskDescription"
                                rows="3" placeholder="Write some text" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="taskImage"
                                class="form-label fw-semibold text-primary-light text-sm mb-8">Attachments <span
                                    class="text-sm">(Jpg, Png format)</span></label>
                            <input type="file" class="form-control" @change="handleFileChange" id="taskImage">
                            <img v-if="currentTask.image" :src="currentTask.image" alt="Image Preview"
                                id="taskImagePreview">
                        </div>
                    </form>
                </div>
                <div class="modal-footer justify-content-center gap-3">
                    <button type="button"
                        class="border border-danger-600 bg-hover-danger-200 text-danger-600 text-md px-50 py-11 radius-8"
                        data-bs-dismiss="modal">
                        Cancel
                    </button>
                    <button type="button" class="btn btn-primary border border-primary-600 text-md px-28 py-12 radius-8"
                        @click="saveTask">
                        Save Changes
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import draggable from 'vuedraggable'
import kanban1 from '@/assets/images/kanban/kanban-1.png'
import kanban2 from '@/assets/images/kanban/kanban-2.png'

const columns = ref([
    {
        title: 'In Progress',
        status: 'inProgress',
        tasks: [
            { id: 1, title: 'Creating a new website', description: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore', tag: 'UI Design', date: '25 Aug 2024', image: kanban1 },
            { id: 2, title: 'Creating a new website', description: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore', tag: 'UI Design', date: '25 Aug 2024', image: kanban2 },
        ],
    },
    {
        title: 'Pending',
        status: 'pending',
        tasks: [
            { id: 3, title: 'Creating a new website', description: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore', tag: 'UI Design', date: '25 Aug 2024' },
            { id: 4, title: 'Creating a new website', description: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore', tag: 'UI Design', date: '25 Aug 2024', image: kanban2 },
        ],
    },
    {
        title: 'Done',
        status: 'done',
        tasks: [
            { id: 5, title: 'Creating a new website', description: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore', tag: 'UI Design', date: '25 Aug 2024' },
            { id: 6, title: 'Creating a new website', description: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore', tag: 'UI Design', date: '25 Aug 2024' },
            { id: 7, title: 'Creating a new website', description: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore', tag: 'UI Design', date: '25 Aug 2024', image: kanban2 },
        ],
    },
    {
        title: 'New',
        status: 'new',
        tasks: [],
    },
])

const currentTask = ref({
    id: null,
    title: '',
    description: '',
    tag: '',
    date: '',
    image: ''
})

const isEditing = ref(false)

function openModal(task = null, status = '') {
    if (task) {
        currentTask.value = { ...task }
        isEditing.value = true
    } else {
        currentTask.value = { id: Date.now(), title: '', description: '', tag: '', date: '', image: '', status: status }
        isEditing.value = false
    }
    const modal = new bootstrap.Modal(document.getElementById('addTaskModal'))
    modal.show()
}

function saveTask() {
    const column = columns.value.find(c => c.status === currentTask.value.status)
    if (isEditing.value) {
        const index = column.tasks.findIndex(t => t.id === currentTask.value.id)
        column.tasks[index] = { ...currentTask.value }
    } else {
        column.tasks.push({ ...currentTask.value })
    }
    const modal = bootstrap.Modal.getInstance(document.getElementById('addTaskModal'))
    modal.hide()
}

function handleFileChange(event) {
    const file = event.target.files[0]
    if (file) {
        const reader = new FileReader()
        reader.onload = () => {
            currentTask.value.image = reader.result
        }
        reader.readAsDataURL(file)
    }
}

function deleteTask(taskId) {
    for (const column of columns.value) {
        const idx = column.tasks.findIndex(t => t.id === taskId)
        if (idx !== -1) {
            column.tasks.splice(idx, 1)
            break
        }
    }
}

function duplicateColumn(column) {
    const duplicatedColumn = {
        ...column,
        title: column.title,
        tasks: [...column.tasks.map(task => ({ ...task, id: Date.now() + Math.random() }))],
    }
    columns.value.push(duplicatedColumn)
}

function deleteColumn(index) {
    columns.value.splice(index, 1)
}
</script>


<style scoped>
.kanban-wrapper {
    display: flex;
}

.kanban-item {
    min-width: 300px;
}

.kanban-card img {
    width: 100%;
    height: auto;
}

.kanban-item:hover,
.kanban-card:hover {
    cursor: move;
}

.vuedraggable-dragging,
.kanban-item:active,
.kanban-card:active {
    cursor: move;
}

/* Style for the ghost placeholder (slot left behind) */
.ghost {
    border: 1px dashed #9e9e9eea;
    background: transparent !important;
    opacity: 1 !important;
    visibility: visible !important;
    min-height: 100px;
    border-radius: 9px;
}

/* Style for the item currently being dragged */
.dragging {
    opacity: 1 !important;
    /* Keep dragged item fully visible */
    z-index: 1000;
    box-shadow: 0 4px 12px rgb(0, 0, 0);
    /* Optional: better visibility */
    transform: none !important;
}
</style>