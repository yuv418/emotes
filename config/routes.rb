Rails.application.routes.draw do
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html

  get ':namespace_slug/:emote_slug', to: 'emote_display#show'
  get ':emote_slug', to: 'emote_display#show'

  namespace :api, defaults: { format: :json } do

    resource :namespace, except: [:create]
    resources :namespaces, except: [:create], param: :slug do
      resources :emotes, param: :slug
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
