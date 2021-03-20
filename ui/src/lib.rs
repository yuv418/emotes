// (Lines like the one below ignore selected Clippy rules
//  - it's useful when you want to check your code with `cargo make verify`
// but some rules are too "annoying" or are not applicable for your case.)
#![allow(clippy::wildcard_imports)]

use seed::{prelude::*, *};
use serde::{Deserialize, Serialize};

const STK: &str = "seeeeeeeeeeeeeeeeeeeeeeed";
// ------ ------
//     Init
// ------ ------

// `init` describes what should happen when your app started.
fn init(_: Url, _: &mut impl Orders<Msg>) -> Model {
    Model {
        todos: LocalStorage::get(STK).unwrap(),
    }
}

// ------ ------
//     Model
// ------ ------

// `Model` describes our app state.
#[derive(Default)]
struct Model {
    todos: Vec<Todo>,
}

#[derive(Serialize, Deserialize)]
struct Todo {
    todo: String,
    #[serde(skip)]
    el: ElRef<web_sys::HtmlInputElement>,
}

// ------ ------
//    Update
// ------ ------

// (Remove the line below once any of your `Msg` variants doesn't implement `Copy`.)
// `Msg` describes the different events you can modify state with.
enum Msg {
    NewTodo,
    ClearTodo,
    DeleteTodo(usize),
    EditTodo(usize, String),
}

// `update` describes how to handle each `Msg`.
fn update(msg: Msg, model: &mut Model, orders: &mut impl Orders<Msg>) {
    match msg {
        Msg::NewTodo => {
            log!("Hi");

            let mut el = ElRef::new();
            let todo = Todo {
                todo: String::default(),
                el: el.clone(),
            };

            model.todos.push(todo);

            orders.after_next_render(move |_| {
                let iel = el.get().unwrap();
                iel.focus();
            });
        }
        Msg::ClearTodo => {
            log!("Clearing todos");
            model.todos.clear();
        }
        Msg::DeleteTodo(index) => {
            let findex = if index == 0 { 0 } else { index - 1 };
            let el_cloned = model.todos[findex].el.clone();
            orders.after_next_render(move |_| {
                let iel = el_cloned.get().unwrap();
                iel.focus();
            });
            model.todos.remove(index);
        }
        Msg::EditTodo(i, newdata) => {
            model.todos[i].todo = newdata;
        }
    }
    LocalStorage::insert(STK, &model.todos);
}

// ------ ------
//     View
// ------ ------

// (Remove the line below once your `Model` become more complex.)
#[allow(clippy::trivially_copy_pass_by_ref)]
// `view` describes what to display.
fn view(model: &Model) -> Node<Msg> {
    div![
        "Todos: ",
        C!["todos"],
        model.todos.iter().enumerate().map(|(i, item)| {
            div![
                input![
                    C!["list"],
                    attrs! {At::Value => item.todo},
                    el_ref(&item.el),
                    input_ev(Ev::Input, move |e| Msg::EditTodo(i, e)),
                    keyboard_ev(Ev::KeyDown, move |kev| {
                        match kev.key().as_str() {
                            "Enter" => Some(Msg::NewTodo),
                            "Delete" => Some(Msg::DeleteTodo(i)),
                            _ => None,
                        }
                    })
                ],
                button!["delete", ev(Ev::Click, move |_| Msg::DeleteTodo(i)),],
            ]
        }),
        button!["new", ev(Ev::Click, |_| Msg::NewTodo),],
        br![],
        button!["clear", ev(Ev::Click, |_| Msg::ClearTodo),],
    ]
}

// ------ ------
//     Start
// ------ ------

// (This function is invoked by `init` function in `index.html`.)
#[wasm_bindgen(start)]
pub fn start() {
    // Mount the `app` to the element with the `id` "app".
    App::start("app", init, update, view);
}
