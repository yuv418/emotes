<template>
    <div class="popular">
        <p><i class="fas fa-poll"></i>Top Rated</p>
        <div v-for="emote in popularEmotes" v-bind:key="emote.id">
            <EmoteBox v-bind:emote="emote"/>
        </div>
    </div>
</template>

<script>
import EmoteBox from './EmoteBox'

export default {
    name: 'Popular',
    components:{EmoteBox},
    data: function() {
        return {
            popularEmotes: [
                {
                id:1,
                name:"fda",
                path:"fdajis"
            },
                {
                id:2,
                name:"fdag",
                path:"fdgajis"
            }
            ]
        };
    }
}
</script>

<style lang="scss">
i{
    font-size: 4rem !important;
    color: #121212;
    height: 2rem;
}
</style>