class Api::ApiKeysController < ApplicationController

  before_action :authenticate

  def create
    new_key = api_key_user.api_keys.new
    if new_key
      new_key.save
      return render json: { jwt: new_key.jwt }
    else
      return render json: { msg: 'The user to make an API key for cannot be found.' }
    end
  end

  def destroy
    begin
      key_data = (JWT.decode params[:delete_key], Rails.application.secret_key_base)[0]
    rescue JWT::DecodeError
      return render json: { msg: "The key you provided to delete was invalid." }, status: :bad_request
    end

    found_key = ApiKey.find key_data["id"] # We're not validating the key since they want to delete it
    if !api_key_user.admin && !(api_key_user.api_keys.include? found_key)
      return render json: { msg: 'You are unauthorized to delete this resource' }, status: :unauthorized
    end

    render json: { msg: 'The API key was deleted successfully.' } if found_key.delete

  end

  private

  def api_key_user
    if params[:username]
      # Administrator is doing things
      User.find_by(find_user_params(params))
    else
      # Regular user self-service
      @current_user
    end
  end

end
