Rails.application.routes.draw do
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html


  namespace :api, defaults: { format: :json } do

    get :namespaces, to: 'namespaces#show'
    resources :namespaces, except: [:show, :create] do
      resources :emotes
    end

    delete :users, to: 'users#destroy'
    resources :users, param: :username, except: :destroy do

      concern :user_actions do
        resources :api_keys, only: [:create]
        delete :api_keys, to: 'api_keys#destroy'

        resources :namespaces, only: [:create]
      end

      collection do
        concerns :user_actions
      end
      concerns :user_actions
    end
  end
end
