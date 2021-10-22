from fastapi import APIRouter, HTTPException, status
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv
from pydantic.types import UUID4
from sqlalchemy.orm.exc import NoResultFound
from starlette import status

from shopping_list.base.settings import get_settings
from shopping_list.models import List, ListUserLink, Share, User
from shopping_list.schemas import CreateShare, CreateShareResponse, ListGet, SharingOptions


router = APIRouter()


@cbv(router)
class ShareHandler:
    @router.post(
        '/users/{user_id}/lists/{list_id}/share',
        status_code=status.HTTP_201_CREATED,
        response_model=CreateShareResponse,
    )
    def share(self, user_id: UUID4, list_id: UUID4, share_options: CreateShare):
        share_item = Share(user_id=user_id, list_id=list_id, share_type=share_options.type)
        session = db.session
        try:
            lst = (
                session.query(List)
                .join(ListUserLink, User)
                .filter(User.user_id == user_id, List.list_id == list_id)
                .one()
            )
        except NoResultFound:
            raise HTTPException(424, "List not found")

        session.add(share_item)
        session.commit()
        return CreateShareResponse(
            share_id=share_item.share_id,
            type=share_item.share_type,
            link=get_settings().SHARE_LINK_TEMPLATE.format(share_id=share_item.share_id),
            qr=get_settings().SHARE_QR_LINK_TEMPLATE.format(share_id=share_item.share_id),
            user_id=user_id,
            list_id=list_id,
        )

    @router.get(
        '/share/{share_id}',
        status_code=status.HTTP_200_OK,
        response_model=ListGet,
    )
    def get_share(self, share_id: UUID4):
        session = db.session
        try:
            share = session.query(Share).filter(Share.share_id == share_id).one()
        except NoResultFound:
            raise HTTPException(404, "Share not found")
        return share.list

    @router.get(
        '/users/{user_id}/share/{share_id}',
        status_code=status.HTTP_202_ACCEPTED,
        response_model=ListGet,
    )
    def accept_share(self, user_id: UUID4, share_id: UUID4):
        session = db.session
        try:
            user = session.query(User).filter(User.user_id == user_id).one()
        except NoResultFound:
            raise HTTPException(404, "User not found")
        try:
            share = session.query(Share).filter(Share.share_id == share_id).one()
        except NoResultFound:
            raise HTTPException(404, "Share not found")

        read_only = share.share_type == SharingOptions.RO
        link = ListUserLink(user_id=user_id, list_id=share.list_id, read_only=read_only)
        session.add(link)
        session.commit()
        return share.list
