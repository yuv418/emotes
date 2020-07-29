<template>
    <div class="EmoteBox">
        <h3>{{ emote.name }}</h3>
        <p>{{emote.path }}</p>
        <img alt="Emote Pic"/>
    </div>
</template>

<script>

export default {
    name: 'EmoteBox',
    props:["emote"],
    data: function() {
        return {
            Emote: null
        };
    },
    methods:{
        getEmote() {
        }
    }
}
</script>

<style lang="scss" scoped>

</style>