<template>
    <div class="search">
        <h2>Browse Emotes</h2>
        <p>Find emotes you're interested in</p>
        <input type="text" placeholder="Oof, JS, Thonk..." v-model="searchField">
        <button v-on:click="getEmotes(searchField)">Search</button>
        <img :src="imageSRC" alt="text"/>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Search',
    data() {
        return {
            imageSRC: "https://emotes.ml/js"
        };
    },
    methods:{
        getEmotes(search) {
            const path = 'https://emotes.ml/' + search;
            axios.get(path)
                .then((res)=>{ 
                    const base64 = btoa(
                    new Uint8Array(res.data).reduce((data, byte) => data + String.fromCharCode(byte),'', ),);
                    this.imageSRC="data:;base64," + base64
                    console.log(this.imageSRC)
                })
                .catch((error)=>{
                    console.error(error)
                })
        }
    }
}
</script>

<style lang="scss" scoped>
h2{
    font-size:2rem;
}
p{
    font-size: 1.25rem;
}
input{
    padding: 0.5rem 1rem;
    border: none;
    border:solid 1px #121212;
    border-radius: 0.5rem;
    font-family: Raleway;
    &:hover{
        border: none;
        border:solid 1px #121212;
        border-radius: 0.5rem;
    }
    &:active{
        border: none;
        border:solid 1px #121212;
        border-radius: 0.5rem;
    }
}
button{
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.5rem;
    color: white;
    background-color: #88BED9;
    font-family: Raleway;
    margin-left:1rem;
    &:hover{
        border: none;
        border-radius: 0.5rem;
    }
    &:active{
        border: none;
        border-radius: 0.5rem;
    }
}
</style>