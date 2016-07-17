SnootyBirdNet::Application.routes.draw do

  # Session Routes
  resources :user_sessions

  match 'login' => "user_sessions#new",      :as => :login
  match 'logout' => "user_sessions#destroy", :as => :logout

  resources :users, :except => [:index,:new,:show,:destroy,:edit] do
    collection do
      get :edit
      get :agreement
    end
  end

  match 'agreement' => 'users#agreement', :as => :agreement
  match 'signup' => 'cocktails#new', :as => :signup

  # Cocktail Resources
  resources :cocktails

  # Admin Routes
  match 'admin' => 'admin#index', :as => :admin

  # Root
  root :to => "front#index"

end
