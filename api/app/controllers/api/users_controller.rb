class Api::UsersController < ApplicationController

  before_action :authenticate
  before_action :admin_authenticate, only: %i[index create]
  before_action only: %i[show delete] do
    validate_owner_or_admin(@user)
  end

  def index
    @users = User.all
    render json: @users
  end

  def show
    @user = User.find_by(find_user_params)
    render json: @user
  end

  def create
    @user = User.new(create_user_params)
    if @user.save
      render json: @user
    else
      render json: @user.errors, status: :bad_request
    end
  end

  def destroy
    @user = User.find_by(find_user_params)
    @user.destroy
    render json: { msg: 'User deleted successfully.' }
  end

  def find_user_params
    super(params)
  end

  private


  def create_user_params
    params.permit(:username)
  end

end
