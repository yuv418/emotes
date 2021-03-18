class EmoteDisplayController < ApplicationController
  def show
    if params[:namespace_slug]
      nmsp = Namespace.find_by slug: params[:namespace_slug]
    else
      nmsp = Namespace.find_by global: true
    end
    emote = nmsp.emotes.find_by slug: params[:emote_slug]

    return render json: { msg: "Emote not found." } unless emote

    width = params[:width]
    height = params[:height]

    width ||= 48
    height ||= 48

    # Size overrides both
    if params[:size]
      begin # We split for any potential security reasons
        width = Integer(params[:size].split("x")[0])
        height = Integer(params[:size].split("x")[1])
      rescue ArgumentError, TypeError
        return render json: { msg: 'Invalid size parameter provided.' }
      end
    end

    rsz_params = "#{width}x#{height}!"

    send_data emote.image.representation(resize: rsz_params).processed.download,
              filename: emote.name,
              content_type: emote.image.content_type,
              disposition: :inline
  end
end
