<template>
    <div class="nav">
        <h1>emotes.ml</h1>
        <div class="navLinks">
            <a href="/">Browse</a>
            <a href="/">Create</a>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Navbar',
}
</script>
<style lang="scss">
.nav{
    overflow: hidden;
    margin: 0;
    text-align: center;
    width: 100%;
    height: auto;
    padding: 1rem 0rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    h1{
        font-size: 1.5rem;
    }
    .navLinks{
        a{
        }
        a:first-child{
            margin-right: 2rem;
        }
    }
}
</style>