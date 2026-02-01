<template>
    <div class="col-xxl-9 col-lg-8">
        <div class="chat-main card overflow-hidden">
            <div class="chat-sidebar-single gap-8 justify-content-between cursor-default flex-nowrap">
                <div class="d-flex align-items-center gap-16">
                    <router-link to="/code-generator-new" class="text-primary-light text-2xl line-height-1">
                        <i class="ri-arrow-left-line"></i>
                    </router-link>
                    <h6 class="text-lg mb-0 text-line-1">{{ header.title }}</h6>
                </div>

                <div class="d-flex align-items-center gap-16 flex-shrink-0">
                    <button type="button" class="text-secondary-light text-xl line-height-1 text-hover-primary-600">
                        <i class="ri-edit-2-line"></i>
                    </button>
                    <button type="button" class="text-secondary-light text-xl line-height-1 text-hover-primary-600">
                        <i class="ri-delete-bin-6-line"></i>
                    </button>
                </div>
            </div>

            <div class="chat-message-list max-h-612-px min-h-612-px">
                <div v-for="(msg, index) in messages" :key="index"
                    class="d-flex align-items-start gap-16 border-bottom border-neutral-200 pb-16 mb-16"
                    :class="msg.justify ? 'justify-content-between' : ''">
                    <div class="d-flex align-items-center gap-16">
                        <div class="img overflow-hidden flex-shrink-0">
                            <img :src="msg.image" alt="image" class="w-44-px h-44-px rounded-circle object-fit-cover" />
                        </div>
                        <div class="info flex-grow-1">
                            <h6 class="text-lg mb-4">{{ msg.name }}</h6>
                            <p v-if="msg.text" class="mb-0 text-secondary-light text-sm">{{ msg.text }}</p>
                            <pre v-if="msg.code" class="language-html mb-16 text-secondary-light text-sm">
  <code>{{ msg.code }}</code>
                </pre>
                        </div>
                    </div>

                    <template v-if="msg.editButton">
                        <button type="button"
                            class="d-flex align-items-center gap-6 px-8 py-4 bg-primary-50 radius-4 bg-hover-primary-100 flex-shrink-0">
                            <i class="ri-edit-2-fill"></i> Edit
                        </button>
                    </template>

                    <template v-if="msg.reactions">
                        <div class="mt-24 d-flex align-items-center justify-content-between gap-16 w-100">
                            <div
                                class="d-flex align-items-center gap-20 bg-neutral-50 radius-8 px-16 py-10 line-height-1">
                                <button v-for="(icon, i) in msg.reactions" :key="i" type="button"
                                    class="text-secondary-light text-2xl d-flex text-hover-info-600">
                                    <i :class="icon"></i>
                                </button>
                            </div>
                            <button type="button" class="btn btn-outline-primary d-flex align-items-center gap-8">
                                <i class="ri-repeat-2-line"></i> Regenerate
                            </button>
                        </div>
                    </template>
                </div>
            </div>

            <form class="chat-message-box">
                <input type="text" name="chatMessage" :placeholder="inputPlaceholder" />
                <button type="submit"
                    class="w-44-px h-44-px d-flex justify-content-center align-items-center radius-8 bg-primary-600 text-white bg-hover-primary-700 text-xl">
                    <iconify-icon :icon="sendIcon"></iconify-icon>
                </button>
            </form>
        </div>
    </div>
</template>

<script>
import chatUser from "@/assets/images/chat/1.png"
import faviconImg from "@/assets/images/wow-dash-favicon.png"
export default {
    data() {
        return {
            header: {
                title: "Please create a 5 Column table with HTML Css and js",
            },
            messages: [
                {
                    name: "Adam Milner",
                    image: chatUser,
                    text: "Please create a 5 Column table with HTML Css and js",
                    editButton: true,
                    justify: true
                },
                {
                    name: "WowDash",
                    image: faviconImg,
                    code: `&lt;<html lang="en">
                            &lt;<head>
                                &lt;<meta charset="UTF-8">
                                &lt;<meta name="viewport" content="width=device-width
                                <link rel="stylesheet" href="styles.css">gt;5 Column <title>5 Column Table</title>
                            &lt;/head&gt;
                            &lt;body&gt;
                                &lt;div class=&quot;table-container&quot;&gt;
                                &lt;table id=&quot;data-table&quot;&gt;
                                    &lt;thead&gt;
                                    &lt;tr&gt;
                                        &lt;th&gt;Column 1&lt;/th&gt;
                                        &lt;th&gt;Column 2&lt;/th&gt;
                                        &lt;th&gt;Column 3&lt;/th&gt;
                                        &lt;th&gt;Column 4&lt;/th&gt;
                                        &lt;th&gt;Column 5&lt;/th&gt;
                                    &lt;/tr&gt;
                                    &lt;/thead&gt;
                                    &lt;tbody&gt;
                                    &lt;!-- Table content goes here --&gt;
                                    &lt;/tbody&gt;
                                &lt;/table&gt;
                                &lt;/div&gt;
                                &lt;script src=&quot;script.js&quot;&gt;&lt;/script&gt;
                            &lt;/body&gt;
                            &lt;/html&gt;`,

                    reactions: [
                        "ri-thumb-up-line",
                        "ri-thumb-down-line",
                        "ri-share-forward-line",
                        "ri-file-copy-line"
                    ]
                },
                {
                    name: "Adam Milner",
                    image: chatUser,
                    text: "Please create a 5 Column table with HTML Css and js",
                    editButton: true,
                    justify: true
                }
            ],
            inputPlaceholder: "Message wowdash...",
            sendIcon: "f7:paperplane"
        };
    }
};
</script>