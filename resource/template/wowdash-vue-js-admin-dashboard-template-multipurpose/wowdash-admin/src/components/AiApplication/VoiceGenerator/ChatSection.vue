<template>
    <div class="col-xxl-9 col-lg-8">
        <div class="chat-main card overflow-hidden">
            <div class="chat-sidebar-single gap-8 justify-content-between cursor-default flex-nowrap">
                <div class="d-flex align-items-center gap-16">
                    <router-link to="/code-generator-new" class="text-primary-light text-2xl line-height-1"><i
                            class="ri-arrow-left-line"></i></router-link>
                    <h6 class="text-lg mb-0 text-line-1">Alright guys, so I've just seen this website...</h6>
                </div>

                <div class="d-flex align-items-center gap-16 flex-shrink-0">
                    <button type="button" class="text-secondary-light text-xl line-height-1 text-hover-primary-600"><i
                            class="ri-edit-2-line"></i></button>
                    <button type="button" class="text-secondary-light text-xl line-height-1 text-hover-primary-600"><i
                            class="ri-delete-bin-6-line"></i></button>
                </div>
            </div>
            <div class="chat-message-list max-h-612-px min-h-612-px">
                <!-- Loop through messages -->
                <div v-for="(msg, index) in messages" :key="index" :class="[
                    'd-flex align-items-start gap-16 border-bottom border-neutral-200 pb-16 mb-16',
                    !msg.audioSrc ? 'justify-content-between' : ''
                ]">
                    <!-- User Text Message -->
                    <template v-if="!msg.audioSrc">
                        <div class="d-flex align-items-start gap-16">
                            <div class="img overflow-hidden flex-shrink-0">
                                <img :src="msg.image" alt="image"
                                    class="w-44-px h-44-px rounded-circle object-fit-cover" />
                            </div>
                            <div class="info">
                                <h6 class="text-lg mb-4">{{ msg.sender }}</h6>
                                <p class="mb-0 text-secondary-light text-sm">{{ msg.message }}</p>
                            </div>
                        </div>
                        <!-- Correct Edit Button Placement -->
                        <button type="button"
                            class="d-flex align-items-center gap-6 px-8 py-4 bg-primary-50 radius-4 bg-hover-primary-100 flex-shrink-0">
                            <i class="ri-edit-2-fill"></i> Edit
                        </button>
                    </template>

                    <!-- Audio Message -->
                    <template v-else>
                        <div class="img overflow-hidden flex-shrink-0">
                            <img :src="msg.image" alt="image" class="w-44-px h-44-px rounded-circle object-fit-cover" />
                        </div>
                        <div class="info flex-grow-1">
                            <h6 class="text-lg mb-16 mt-8">{{ msg.sender }}</h6>
                            <div class="audioplayer">
                                <audio :src="msg.audioSrc" preload="auto" controls></audio>
                            </div>
                            <div class="mt-24 d-flex align-items-center gap-16">
                                <button type="button"
                                    class="btn btn-primary d-flex align-items-center gap-8 px-20 flex-shrink-0">
                                    Download
                                    <i class="ri-download-2-line"></i>
                                </button>
                                <select class="form-select form-control min-w-132-px px-16 py-14 h-48-px w-auto">
                                    <option value="">Mp3</option>
                                    <option value="">Mp4</option>
                                </select>
                            </div>
                        </div>
                    </template>
                </div>
            </div>
            <form class="chat-message-box">
                <input type="text" name="chatMessage" placeholder="Message wowdash...">
                <button type="submit"
                    class="w-44-px h-44-px d-flex justify-content-center align-items-center radius-8 bg-primary-600 text-white bg-hover-primary-700 text-xl">
                    <iconify-icon icon="f7:paperplane"></iconify-icon>
                </button>
            </form>
        </div>
    </div>
</template>

<script>
import chatUser from "@/assets/images/chat/1.png"
import favicon from "@/assets/images/wow-dash-favicon.png"
export default {
    data() {
        return {
            message: '',
            messages: [
                {
                    sender: "Adam Milner",
                    message:
                        "Alright guys, so I've just seen this website, Fortunanest website, it's an investment website and you invest there. So I actually tried it some months, I tried it just for 3 months and I realized everything was working correct. I was thinking it was this fake website, I never met this website.",
                    image: chatUser
                },
                {
                    sender: "WowDash",
                    audioSrc: "https://www.w3schools.com/html/horse.mp3",
                    image: favicon
                }
            ]
        };
    },
    methods: {
        sendMessage() {
            console.log("Sending message:", this.message);
            this.message = '';
        }
    }
};
</script>
<style>
.audioplayer{
    display: flex;
    flex-direction: row;
    box-sizing: border-box;
    margin: 1em 0;
    padding: 0 24px;
    width: 100%;
    height: 96px;
    align-items: center;
    border: 1px solid #DDE2E6;
    border-radius: 50px;
    background: #fff;
}
</style>