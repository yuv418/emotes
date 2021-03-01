class Api::NamespacesController < ApplicationController
  before_action :authenticate
  before_action :admin_authenticate, only: [:index]

  def index
    render json: Namespace.all
  end

  def show
    render json: Namespace.find_by(find_namespace_params)
  end

  def create
    user = User.find_by(find_user_params(params))
    nmsp = user.namespaces.new(create_namespace_params)

    if nmsp.save
      return render json: nmsp
    else
      return render json: nmsp.errors, status: :bad_request
    end
  end

  def destroy
  end

  def update
  end

  private

  def create_namespace_params
    params.permit(:slug)
  end

  def find_namespace_params
    params.permit(:id, :slug)
  end
end


