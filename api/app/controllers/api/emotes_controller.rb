class Api::EmotesController < ApplicationController
  def create
    nmsp = Namespace.find_by(params[:namespace_slug])
    emote = nmsp.emotes.new create_emote_params

    if emote.save
      render json: emote
    else
      render json: emote.errors, status: :bad_request
    end
  end

  def delete
    nmsp = Namespace.find_by(params[:namespace_slug])
    emote = nmsp.emotes.find_by slug: params[:slug]

    if emote.delete
      render json: { msg: 'Emote deleted.' }
    else
      render json: emote.errors
    end
  end

  private

  def create_emote_params
    params.permit(:slug, :name, :image, :emote_type)
  end

end
