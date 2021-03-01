class ApplicationController < ActionController::API

  protected

  def authenticate
    begin
      api_key_info = JWT.decode params["key"], Rails.application.secret_key_base
    rescue JWT::DecodeError
      return render json: { msg: 'Invalid API key provided.' }, status: 401
    end
    api_key = ApiKey.find api_key_info[0]["id"]

    @api_key = api_key&.authenticate_key(api_key_info[0]["key"])
    if @api_key
      @current_user = @api_key.user if @api_key.user
    else
      return render json: { msg: 'You are not authorized to access this resource' }, status: 401
    end
  end

  def admin_authenticate
    unless @current_user.admin
      return render json: { msg: 'You are not an admin and therefore are unauthorized to access this resource' }, status: 401
    end
  end

  def validate_owner_or_admin(user)
    unless @current_user.admin || @current_user == user
      return render json: { msg: 'You are unauthorized to access this resource' }, status: 401
    end
    true
  end

  def find_user_params(params)
    params.permit(:id, :username)
  end

end
